import Cocoa
import WebKit

final class AppDelegate: NSObject, NSApplicationDelegate, WKScriptMessageHandler, WKNavigationDelegate, WKUIDelegate {
    var window: NSWindow!
    var web: WKWebView!
    let runner = DispatchQueue(label: "study.switch.runner")
    func applicationDidFinishLaunching(_ notification: Notification) {
        let menu = NSMenu(); let item = NSMenuItem(); menu.addItem(item)
        let appMenu = NSMenu(); appMenu.addItem(withTitle: "About Switch", action: #selector(NSApplication.orderFrontStandardAboutPanel(_:)), keyEquivalent: "")
        appMenu.addItem(NSMenuItem.separator()); appMenu.addItem(withTitle: "Quit Switch", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q"); item.submenu = appMenu
        let edit = NSMenuItem(); menu.addItem(edit); edit.submenu = NSMenu(title: "Edit")
        for (title, action, key) in [("Undo", "undo:", "z"), ("Cut", "cut:", "x"), ("Copy", "copy:", "c"), ("Paste", "paste:", "v"), ("Select All", "selectAll:", "a")] { edit.submenu?.addItem(withTitle: title, action: Selector(action), keyEquivalent: key) }
        NSApp.mainMenu = menu
        let config = WKWebViewConfiguration()
        config.userContentController.addUserScript(WKUserScript(source: "window.switchCapabilities = {cppApiVersion: 2, appVersion: '2.3.0'};", injectionTime: .atDocumentStart, forMainFrameOnly: true))
        config.userContentController.add(self, name: "runCode"); config.userContentController.add(self, name: "export")
        web = WKWebView(frame: .zero, configuration: config); web.navigationDelegate = self; web.uiDelegate = self
        window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 1280, height: 860), styleMask: [.titled,.closable,.miniaturizable,.resizable], backing: .buffered, defer: false)
        window.title = "Switch — Your next move"; window.minSize = NSSize(width: 780, height: 600); window.contentView = web; window.center(); window.makeKeyAndOrderFront(nil)
        let root = Bundle.main.resourceURL!.appendingPathComponent("web")
        web.loadFileURL(root.appendingPathComponent("index.html"), allowingReadAccessTo: root)
        NSApp.activate(ignoringOtherApps: true)
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }
    func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        guard let url = action.request.url else { decisionHandler(.cancel); return }
        if ["https", "http"].contains(url.scheme ?? "") { NSWorkspace.shared.open(url); decisionHandler(.cancel) } else if url.isFileURL && url.path.hasPrefix(Bundle.main.resourceURL!.path) { decisionHandler(.allow) } else { decisionHandler(.cancel) }
    }
    func webView(_ webView: WKWebView, createWebViewWith configuration: WKWebViewConfiguration, for action: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
        if let url = action.request.url, ["https","http"].contains(url.scheme ?? "") { NSWorkspace.shared.open(url) }; return nil
    }
    func webView(_ webView: WKWebView, runOpenPanelWith parameters: WKOpenPanelParameters, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping ([URL]?) -> Void) {
        let panel=NSOpenPanel(); panel.allowsMultipleSelection=false; panel.canChooseDirectories=false
        panel.beginSheetModal(for: window) { result in completionHandler(result == .OK ? panel.urls : nil) }
    }
    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        guard message.frameInfo.isMainFrame, message.frameInfo.request.url?.isFileURL == true else { return }
        if message.name == "export", let text=message.body as? String {
            let panel=NSSavePanel(); panel.nameFieldStringValue="switch-progress.json"
            panel.beginSheetModal(for: window) { result in if result == .OK, let url=panel.url { do { try text.write(to:url,atomically:true,encoding:.utf8) } catch { self.alert(error.localizedDescription) } } }; return
        }
        guard message.name == "runCode", let body=message.body as? [String:Any], let id=body["id"] as? String, let language=body["language"] as? String, let code=body["code"] as? String, let input=body["input"] as? String, code.utf8.count < 500000, input.utf8.count < 1000000 else { return }
        runner.async {
            let result=self.execute(language:language,code:code,input:input,practice:body["practice"] as? Bool ?? false,problemId:body["problemId"] as? String)
            DispatchQueue.main.async {
                if let json=try? JSONSerialization.data(withJSONObject:[id,result]), let args=String(data:json,encoding:.utf8) { self.web.evaluateJavaScript("window.switchNativeResult(...\(args))",completionHandler:nil) }
            }
        }
    }
    func alert(_ text:String) { let a=NSAlert(); a.messageText=text; a.runModal() }
    func executable(_ name:String)->String? {
        for dir in ["/opt/homebrew/bin","/usr/local/bin","/usr/bin","/bin"] { let p=dir+"/"+name;if FileManager.default.isExecutableFile(atPath:p){return p} }; return nil
    }
    func invoke(_ program:String,_ args:[String],_ directory:URL,_ stdin:String,_ seconds:Double)->(Int32,String) {
        let fm=FileManager.default, inputURL=directory.appendingPathComponent(UUID().uuidString+".in"), outputURL=directory.appendingPathComponent(UUID().uuidString+".out")
        do {
            try stdin.write(to:inputURL,atomically:true,encoding:.utf8);fm.createFile(atPath:outputURL.path,contents:nil)
            let input=try FileHandle(forReadingFrom:inputURL),output=try FileHandle(forWritingTo:outputURL)
            defer {try? input.close();try? output.close()}
            let p=Process();p.executableURL=URL(fileURLWithPath:"/bin/sh");p.arguments=["-c","ulimit -t \(Int(seconds)+1); ulimit -f \(seconds >= 30 ? 65536 : 2048); exec \"$@\"","switch-runner",program]+args;p.currentDirectoryURL=directory
            var env=ProcessInfo.processInfo.environment;env["PATH"]="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin";p.environment=env;p.standardInput=input;p.standardOutput=output;p.standardError=output
            try p.run();let until=Date().addingTimeInterval(seconds)
            while p.isRunning && Date()<until {Thread.sleep(forTimeInterval:0.03)}
            if p.isRunning {p.terminate();Thread.sleep(forTimeInterval:0.1);if p.isRunning {kill(p.processIdentifier,SIGKILL)};p.waitUntilExit();return (-1,"Time limit exceeded. Check loops and recursion.")}
            let data=(try? Data(contentsOf:outputURL)) ?? Data();let text=String(decoding:data.prefix(65536),as:UTF8.self)
            return (p.terminationStatus,text+(data.count>65536 ? "\n[Output truncated]" : ""))
        }catch{return (-1,error.localizedDescription)}
    }
    func execute(language:String,code:String,input:String,practice:Bool = false,problemId:String? = nil)->String {
        let dir=FileManager.default.temporaryDirectory.appendingPathComponent("switch-"+UUID().uuidString)
        do {
            try FileManager.default.createDirectory(at:dir,withIntermediateDirectories:true);defer{try? FileManager.default.removeItem(at:dir)}
            var program:String;var args:[String]
            switch language {
            case "python":
                guard let python=executable("python3") else{return "Python 3 is not installed. Install Python 3, or use the built-in JavaScript runner."}
                let suffix = practice ? (try String(contentsOf:Bundle.main.resourceURL!.appendingPathComponent("include/harness.py"),encoding:.utf8)) : ""
                try (code+"\n"+suffix).write(to:dir.appendingPathComponent("main.py"),atomically:true,encoding:.utf8);program=python;args=["-I","main.py"]
            case "cpp":
                guard let compiler=executable("clang++") else{return "C++ compiler not found. Install Xcode Command Line Tools."}
                let includeDir=Bundle.main.resourceURL!.appendingPathComponent("include")
                let suffix=practice ? (try String(contentsOf:includeDir.appendingPathComponent("harness.cpp"),encoding:.utf8)) : ""
                let prefix=practice ? "#include \"switch_runtime.hpp\"\n" : ""
                var adapter=""
                if practice {
                    let data=try Data(contentsOf:includeDir.appendingPathComponent("cpp-adapters.json"))
                    let adapters=try JSONDecoder().decode([String:String].self,from:data)
                    guard let id=problemId,let source=adapters[id] else { return "This problem has no C++ test runner. Reopen it in the updated app." }
                    adapter=source
                }
                try (prefix+"#line 1 \"solution.cpp\"\n"+code+"\n#line 1 \"runner.cpp\"\n"+adapter+"\n"+suffix).write(to:dir.appendingPathComponent("main.cpp"),atomically:true,encoding:.utf8)
                let (status,text)=invoke(compiler,["-std=c++17","-O0","-I",includeDir.path,"main.cpp","-o","main"],dir,"",30)
                if status != 0{return "Compilation failed:\n"+text};program=dir.appendingPathComponent("main").path;args=[]
            case "java":
                guard let compiler=executable("javac"),let java=executable("java") else{return "Java JDK not found. Install a JDK or use JavaScript."}
                try code.write(to:dir.appendingPathComponent("Main.java"),atomically:true,encoding:.utf8)
                let(status,text)=invoke(compiler,["Main.java"],dir,"",8)
                if status != 0{return "Compilation failed (a JDK is required):\n"+text};program=java;args=["-Xmx128m","-cp",dir.path,"Main"]
            default:return "Unsupported language"
            }
            let(status,text)=invoke(program,args,dir,input,5);return text+(status==0 ? (text.isEmpty ? "Completed with no output." : "") : "\nExit status: \(status)")
        }catch{return error.localizedDescription}
    }
}
if CommandLine.arguments.contains("--self-test") {
    let runner=AppDelegate()
    let cases="[{\"input\":[3,1,7,2],\"expected\":7},{\"input\":[-8,-3],\"expected\":-3}]"
    let python=runner.execute(language:"python",code:"def solve(input):\n    return max(input)",input:cases,practice:true)
    print("Python runner:\n"+python)
    var passed=python.contains("TEST 2: PASS") && !python.contains("FAIL") && !python.contains("ERROR")
    do {
        let data=try Data(contentsOf:Bundle.main.resourceURL!.appendingPathComponent("include/cpp-smoke.json"))
        guard let samples=try JSONSerialization.jsonObject(with:data) as? [[String:Any]], !samples.isEmpty else { exit(1) }
        for sample in samples {
            guard let id=sample["id"] as? String,let code=sample["code"] as? String,let tests=sample["tests"] as? [[String:Any]] else { exit(1) }
            let input=String(decoding:try JSONSerialization.data(withJSONObject:tests),as:UTF8.self)
            let output=runner.execute(language:"cpp",code:code,input:input,practice:true,problemId:id)
            print("C++ \(id):\n"+output)
            passed = passed && output.contains("TEST \(tests.count): PASS") && !output.contains("FAIL") && !output.contains("ERROR")
        }
    } catch { print(error.localizedDescription); passed=false }
    exit(passed ? 0 : 1)
}
let app=NSApplication.shared
let delegate=AppDelegate();app.delegate=delegate
app.setActivationPolicy(.regular)
app.run()
