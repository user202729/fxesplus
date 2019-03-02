#include<iostream>
#include<fstream>
#include<string>
#include<string_view>
#include<vector>
#include<algorithm>
#include<unordered_map>

/*
C++ implementation of brief_match.py.

nnoremap <leader>c :up<bar>!xterm -e 'g++ -std=c++17 -g -D_GLIBCXX_DEBUG -Wall -Wconversion  -fsanitize=undefined "%" <bar><bar> read' &<CR><CR>
nnoremap <leader>o :up<bar>!xterm -e 'g++ -std=c++17 -O2 "%" <bar><bar> read' &<CR><CR>
*/
int last_num=0;
std::unordered_map<std::string,int> line_to_num;

std::pair<std::vector<std::string>,std::vector<int>> read_file(char const* filename){
	// Read disassembly commands and address from filename.

	std::vector<int> commands;
	std::vector<std::string> linenums;
	std::ifstream f(filename);std::string x;
		while(std::getline(f,x)){
			linenums.push_back(x.substr(0,6));
			x=x.substr(28);
			auto iter=line_to_num.find(x); if(iter==line_to_num.end()){
				last_num+=1;
				line_to_num.emplace(x,last_num);
				commands.push_back(last_num);
			}else
				commands.push_back(iter->second); }
	return {std::move(linenums),std::move(commands)}; }

template<class Iter>int find_sublist(Iter af,Iter al,Iter bf,Iter bl){
	for(auto x=bl-bf-(al-af),i=0;i<=x;++i)
		if(std::equal(af,al,bf+i))
			return i;
	return -1; }

struct T{int i1,nline,i2;};template<class CmdT>auto process(std::vector<CmdT> l1,std::vector<CmdT> l2){
	std::vector<T> result; // list of (line index 1, number of lines, line index 2)
	int last_end=0;
	for(int i=0;i<(int)l1.size();++i){
		int end=std::max(last_end,i),good_index;
		while(end!=(int)l1.size()){
			int index=find_sublist(l1.begin()+i,l1.begin()+end+1,l2.begin(),l2.end());
			if(index<0)
				break;
			good_index=index;
			while(end!=(int)l1.size() && l1[end]==l2[index-i+end])
				end+=1; }
		if(end>last_end){
			last_end=end;
			if(find_sublist(l1.begin()+i,l1.begin()+end,l2.begin()+good_index+1,l2.end())<0)
				// unique appearance
				result.push_back({i,end-i,good_index}); }}
	return result; }

int main(int argc,char** argv){

	if(argc!=3){
		std::cerr<<"Wrong number of arguments\n";
		return 1; }

	auto [l1num,l1]=read_file(argv[1]);
	auto [l2num,l2]=read_file(argv[2]);

	for(auto [i,length,j]:process(l1,l2))
		std::cout<<"["<<l1num[i]<<" .. "<<l1num[i+length]<<"] --> ["<<l2num[j]<<" ..]\n";
}
