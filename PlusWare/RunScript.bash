MainFile="main.cpp"
ToCompileList=$(find "./Helpers" -type f -name '*.cpp' -print)

printf 'These files will be compiled:\n%s\n' "$ToCompileList, $MainFile"

g++ -o PluswareCompiled $MainFile $ToCompileList  -std=c++17

./PluswareCompiled
