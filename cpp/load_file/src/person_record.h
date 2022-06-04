#ifndef __PERSON_RECORD_H_DEFINED__
#define __PERSON_RECORD_H_DEFINED__

#include <string>
#include <memory>
#include <vector>
#include <map>
#include <stdexcept>
#include <charconv>
#include <boost/range.hpp>
#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>
#include <fmt/format.h>

struct PersonRecord
{
public:
    int Id;
    std::string first_name;
    std::string last_name;
    std::string phone_number;
    int age;
    int salary;

    using UPtr = std::unique_ptr<PersonRecord>;
    static UPtr Parse(const std::string& input)
    {
        namespace ba = boost::algorithm;
        using cit_range = boost::iterator_range<const char *>;
        using cit_range_vec = std::vector<cit_range>;
        cit_range_vec words;
        ba::split(words, input.data(), ba::is_any_of(" \t"));
        if (words.size() < 6)
            throw std::runtime_error(fmt::format("could not parse {}", input));

        auto as_int = [](cit_range &range) ->int {
            int val;
            if (static_cast<int>(std::from_chars(range.begin(),range.end(), val).ec))
                throw std::runtime_error("could not convert to int");
            return val;
        };
        return UPtr(new PersonRecord{
            as_int(words[0]),
            std::string(words[1].begin(),words[1].size()),
            std::string(words[2].begin(),words[2].size()),
            std::string(words[3].begin(),words[3].size()),
            as_int(words[4]),
            as_int(words[5])
        });
    }
    inline static boost::regex gRegExPersonRec{R"(\s*(\d+)\s+(\w+)\s+(\w+)\s+(\S+)\s+(\d+)\s+(\d+))"};
    static UPtr ParseRegex(const std::string &input)
    {
        boost::cmatch words;
        if(!boost::regex_search(input.c_str(),words,gRegExPersonRec))
            throw std::runtime_error(fmt::format("could not parse {} \n",input));
        auto as_int = [](const boost::csub_match &cm)->int{
            int val;
            if(static_cast<int>(std::from_chars(cm.first,cm.second,val).ec))
                throw std::runtime_error("could not convert to int");
            return val;
        };
        return UPtr(new PersonRecord{
            as_int(words[1]),
            words[2].str(),
            words[3].str(),
            words[4].str(),
            as_int(words[5]),
            as_int(words[6])
        });
    }
};

#endif // __PERSON_RECORD_H_DEFINED__
