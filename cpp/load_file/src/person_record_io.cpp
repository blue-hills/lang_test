#include "person_record_io.h"
#include <argparse/argparse.hpp>
#include <fmt/format.h>

struct ProgramArgs
{
    int repeat_count;
    std::string input_file;
    std::string algorithm;

    static ProgramArgs GetArgs(int argc,char *argv[])
    {
        argparse::ArgumentParser program("FileLoader");
        program.add_argument("-r","--repeat").help("Repeat Count").default_value<int>(1000).scan<'i', int>();
        program.add_argument("-i","--input").help("InputFile").required().default_value(false);
        program.add_argument("-a","--algo").default_value("split")
            .action([](const std::string& value) {
                static const std::vector<std::string> choices = { "split","regex"};
                if (std::find(choices.begin(), choices.end(), value) != choices.end()) {
                  return value;
                }
                return std::string{ "split" };
              });
        program.parse_args(argc,argv);
        return ProgramArgs{
                program.get<int>("repeat"),
                program.get<std::string>("input"),
                program.get<std::string>("algo")
            };
    }
};

class TestRunner
{
    public:
    static void RunTests(const ProgramArgs &prog_args)
    {
        using ParseFunc = PersonRecord::UPtr (*)(const std::string &);
        ParseFunc func = prog_args.algorithm == "regex" ? &PersonRecord::ParseRegex : &PersonRecord::Parse;
        
        for (auto count = 0; count < prog_args.repeat_count; ++count)
        {
            auto dict = PersonRecordIO::CreatePersonRecordDictFromFile(prog_args.input_file,func);
            if (dict->find(dict->size() - 1) == dict->end())
            {
                throw std::runtime_error(fmt::format("Could not find record for {} ", dict->size() - 1));
            }
        }
        std::cout << fmt::format("Executed {} times successfully\n",prog_args.repeat_count) ;   
        std::cout << fmt::format("{} has been used for parsing.\n",
            (prog_args.algorithm == "regex" ? "boost::regex" : "boost::algorithm::split"));
    }    
};

int main(int argc, char* argv[])
{
    try
    {
        auto prog_args = ProgramArgs::GetArgs(argc,argv);
        TestRunner::RunTests(prog_args);
    }
    catch (const std::exception& e)
    {
        std::cout << e.what() << std::endl;
    }

    return 0;
}
