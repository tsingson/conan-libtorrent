cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)
project(conan-libtorrent)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

include_directories(${CMAKE_SOURCE_DIR}/libtorrent-libtorrent-1_1/include)
add_subdirectory(libtorrent-libtorrent-1_1)
