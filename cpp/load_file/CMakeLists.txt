cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(load_person_record_file LANGUAGES CXX C)


if(NOT EXISTS ${THIRD_PARTY_SOURCE})
    if(EXISTS $ENV{THIRD_PARTY_SOURCE})
        set(THIRD_PARTY_SOURCE $ENV{THIRD_PARTY_SOURCE} )
    elseif(EXISTS "/usr/local/src")
        set(THIRD_PARTY_SOURCE /usr/local/src)
    else()
        message("THIRD_PARTY_SOURCE variable is not defined.")
        message("Define in command line -DTHIRD_PARTY_SOURCE=path")
        message("Or Define using environment variable export THIRD_PARTY_SOURCE=path")
    endif()        
endif()

if(NOT EXISTS ${BOOST_SOURCE})
    if(EXISTS $ENV{BOOST_SOURCE})
        set(BOOST_SOURCE $ENV{BOOST_SOURCE} )
    else()
        message("BOOST_SOURCE variable is not defined.")
        message("Define in command line -DBOOST_SOURCE=path")
        message("Or Define using environment variable export BOOST_SOURCE=path")    
    endif()
endif()

#check if all  thirdparty directories are available or not
function(validate_path path)
    if(NOT EXISTS ${path})
        message(FATAL_ERROR "path ${path} does not exist")
    endif()
endfunction()

validate_path("${THIRD_PARTY_SOURCE}/fmt-master/include")
validate_path("${THIRD_PARTY_SOURCE}/argparse-master/include")
validate_path("${BOOST_SOURCE}/boost/algorithm")
validate_path("${BOOST_SOURCE}/boost/regex")

message( "build system : ${CMAKE_SYSTEM_NAME} ,Third Party Source : ${THIRD_PARTY_SOURCE}")
add_executable(load_person_record_file)

add_compile_definitions(FMT_HEADER_ONLY BOOST_REGEX_STANDALONE)

set_target_properties(load_person_record_file 
  PROPERTIES
  CXX_STANDARD 17
  CXX_EXTENSIONS OFF
  CXX_STANDARD_REQUIRED ON
)

if(NOT CMAKE_BUILD_TYPE  OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O2")


target_include_directories(load_person_record_file 
   PRIVATE ${THIRD_PARTY_SOURCE}/fmt-master/include
   PRIVATE ${BOOST_SOURCE}
   PRIVATE ${THIRD_PARTY_SOURCE}/argparse-master/include
   PRIVATE ${CMAKE_CURRENT_LIST_DIR}/src
)

target_sources(load_person_record_file
 PRIVATE ${CMAKE_CURRENT_LIST_DIR}/src/person_record_io.cpp 
)
