#include <fstream>
int main(int argc, char** argv) {
    json report = {{"results", json::array()}};
    try {
        json cases; std::cin >> cases;
        int index = 0;
        for (const auto& test : cases) {
            ++index;
            try {
                json actual = switchSolve(test.at("input"));
                bool custom = !test.contains("expected");
                report["results"].push_back({{"index", index}, {"pass", !custom && actual == test["expected"]}, {"actual", actual}});
                std::cout << (custom ? "OUTPUT" : "TEST " + std::to_string(index) + ": " + (actual == test["expected"] ? "PASS" : "FAIL")) << "\n" << actual.dump(2) << "\n";
                if (!custom && actual != test["expected"]) std::cout << "Expected: " << test["expected"].dump() << "\n";
            } catch (const std::exception& e) {
                report["results"].push_back({{"index", index}, {"pass", false}, {"error", e.what()}});
                std::cout << "TEST " << index << ": ERROR\n" << e.what() << "\n";
            }
        }
    } catch (const std::exception& e) { std::cerr << e.what() << "\n"; return 1; }
    if (argc > 1) { std::ofstream file(argv[1]); file << report.dump(); }
}
