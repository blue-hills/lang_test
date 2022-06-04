cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(load_person_record_file LANGUAGES CXX C)


set(THIRD_PARTY_SOURCE /usr/local/src)


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
   PRIVATE ${THIRD_PARTY_SOURCE}/boost_1_79_0
   PRIVATE ${THIRD_PARTY_SOURCE}/argparse-master/include
   PRIVATE ${CMAKE_CURRENT_LIST_DIR}/src
)

target_sources(load_person_record_file
 PRIVATE ${CMAKE_CURRENT_LIST_DIR}/src/person_record_io.cpp 
)
