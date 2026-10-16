import AppKit
let root=CommandLine.arguments[1]
let directory=URL(fileURLWithPath:root).appendingPathComponent("Switch.iconset")
try FileManager.default.createDirectory(at:directory,withIntermediateDirectories:true)
for size in [16,32,128,256,512] {
    for scale in [1,2] {
        let pixels=size*scale
        let bitmap=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:pixels,pixelsHigh:pixels,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
        NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:bitmap)
        let transform=AffineTransform(scale:CGFloat(pixels)/128);(transform as NSAffineTransform).concat()
        NSColor(calibratedRed:40/255,green:97/255,blue:75/255,alpha:1).setFill()
        NSBezierPath(roundedRect:NSRect(x:4,y:4,width:120,height:120),xRadius:28,yRadius:28).fill()
        NSColor(calibratedRed:217/255,green:237/255,blue:180/255,alpha:1).setStroke()
        let arrow=NSBezierPath();arrow.lineWidth=12;arrow.lineCapStyle = .round;arrow.lineJoinStyle = .round
        arrow.move(to:NSPoint(x:38,y:38));arrow.line(to:NSPoint(x:87,y:87));arrow.move(to:NSPoint(x:44,y:87));arrow.line(to:NSPoint(x:87,y:87));arrow.line(to:NSPoint(x:87,y:44));arrow.stroke()
        NSGraphicsContext.restoreGraphicsState()
        let name="icon_\(size)x\(size)"+(scale==2 ? "@2x" : "")+".png"
        try bitmap.representation(using:.png,properties:[:])!.write(to:directory.appendingPathComponent(name))
    }
}
