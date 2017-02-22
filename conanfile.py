import os
from conans import ConanFile, CMake, ConfigureEnvironment
from conans.tools import download, unzip, replace_in_file

def tagFromVersion(version):
    '''
    @arg version = "{major_version}.{minor_version}.{__version}"
    returns "{major_version}_{minor_version}"
    '''
    version = version.split('.')
    return version[0] + "_" + version[1]

class LibtorrentConan(ConanFile):
    name = "libtorrent"
    version = "1.1.0"
    generators = "cmake"
    tagged_version = tagFromVersion(version)
    ZIP_FOLDER_NAME = "%s-%s" % (name, tagged_version)
    build_directory = ""
    settings = "os", "compiler", "build_type", "arch"
    exports = ["CMakeLists.txt", "libtorrent-rasterbar.cmake.pc.in", "libtorrent-rasterbar.pc.in", "FindLibtorrentRasterbar.cmake"]
    options = {"shared": [True, False],
               "enable_crypto": [True, False],
               "enable_data": [True, False],
               "enable_data_sqlite": [True, False],
               "enable_data_odbc": [True, False],
               "enable_zip": [True, False],
               "force_openssl": [True, False], #  "Force usage of OpenSSL even under windows"
               "enable_tests": [True, False],
               "cxx_14": [True, False]
               }
    default_options = '''
shared=False
enable_crypto=True
enable_data=False
enable_data_sqlite=True
enable_data_odbc=False
enable_zip=True
force_openssl=True
enable_tests=False
cxx_14=False
'''

    def source(self):
        zip_name = "libtorrent-%s.zip" % self.tagged_version
        download("http://github.com/arvidn/libtorrent/archive/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)

        self.build_directory = self.conanfile_directory

        self.output.warn('cmake %s %s' % (self.conanfile_directory, cmake.command_line))
        self.run('cmake %s %s' % (self.conanfile_directory, cmake.command_line))

        self.output.warn('cmake %s %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        # Copy findZLIB.cmake to package
        self.copy("FindLibtorrentRasterbar.cmake", ".", ".")

        # Copy libtorrent header files
        #TODO: Copy the header files to package/include without preserving paths.
        '''
        self.copy("*.hpp", dst="include", src="%s" % self.ZIP_FOLDER_NAME)
        self.copy(pattern="*.hpp", dst="include/libtorrent", src="%s/libtorrent-%s/include/libtorrent" % (self.source_directory, self.ZIP_FOLDER_NAME))
        '''
        self.copy("*.hpp", dst="include")

        # Copy libtorrent libraries
        self.copy(pattern="*.a",   dst="lib", src="%s/libtorrent-%s" % (self.build_directory, self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="%s/libtorrent-%s" % (self.build_directory, self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="%s/libtorrent-%s" % (self.build_directory, self.ZIP_FOLDER_NAME), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["torrent-rasterbar"]
