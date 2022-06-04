#ifndef __PERSON_RECORD_IO_H_DEFINED__
#define __PERSON_RECORD_IO_H_DEFINED__

#include <map>
#include <fstream>
#include "person_record.h"

class PersonRecordIO
{
    public:
    using PersonRecordDict = std::map<int, PersonRecord::UPtr>;
    template <typename ParseFunc>
    static std::unique_ptr<PersonRecordDict> CreatePersonRecordDictFromFile(const std::string& filename,ParseFunc parse_func)
    {
        std::ifstream stream;
        char streambuff[8 * 1024];
        stream.rdbuf()->pubsetbuf(streambuff, sizeof(streambuff));
        stream.open(filename.data());
        std::string line;
        line.reserve(128);
        auto dict = std::make_unique<PersonRecordDict>();
        while (std::getline(stream, line))
        {
            auto record = parse_func(line);
            dict->emplace(record->Id, std::move(record));
        }
        return dict;
    }
};
#endif //__PERSON_RECORD_IO_H_DEFINED__
