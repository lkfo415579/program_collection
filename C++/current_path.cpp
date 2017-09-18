#include <windows.h>
#include <string>
#include <vector>
#include <stack>
#include <iostream>

#include <sstream>
#include <fstream>
#include <locale>

using namespace std;

bool ListFiles(wstring path, wstring mask, vector<wstring>& files) {
	HANDLE hFind = INVALID_HANDLE_VALUE;
	WIN32_FIND_DATA ffd;
	wstring spec;
	stack<wstring> directories;

	directories.push(path);
	files.clear();

	while (!directories.empty()) {
		path = directories.top();
		spec = path + L"\\" + mask;
		directories.pop();

		hFind = FindFirstFile(spec.c_str(), &ffd);
		if (hFind == INVALID_HANDLE_VALUE) {
			return false;
		}

		do {
			if (wcscmp(ffd.cFileName, L".") != 0 &&
				wcscmp(ffd.cFileName, L"..") != 0) {
				if (ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
					directories.push(path + L"\\" + ffd.cFileName);
				}
				else {
					files.push_back(path + L"\\" + ffd.cFileName);
				}
			}
		} while (FindNextFile(hFind, &ffd) != 0);

		if (GetLastError() != ERROR_NO_MORE_FILES) {
			FindClose(hFind);
			return false;
		}

		FindClose(hFind);
		hFind = INVALID_HANDLE_VALUE;
	}

	return true;
}
/*
vector<wstring> &split(const wstring &str, char delim, vector<wstring> &elems, bool skip_empty = true) {
	istringstream iss(str);
	for (wstring item; getline(iss, item, delim); )
		if (skip_empty && item.empty()) continue;
		else elems.push_back(item);
		return elems;
}*/

vector<wstring> &split(const wstring &str, wchar_t delim, vector<wstring> &elems) {
	wstring tmp;
	for (auto& it : str)
	{
		if (it != delim) {
			tmp.push_back(it);
		}
		else {
			elems.push_back(tmp);
			tmp = L"";
		}
	}
	elems.push_back(tmp);
	return elems;
}

wstring ExePath() {
	TCHAR pwd[MAX_PATH];
	GetCurrentDirectory(MAX_PATH, pwd);
	wstring tmp;
	for (size_t i = 0; pwd[i] != 52428 && pwd[i] != 0; i++)
	{
		tmp.push_back(pwd[i]);
		//pwd[i]
	}
	
	//tmp.erase(tmp.end());
	//string tmp(pwd);
	return tmp;
}
int main(int argc, char* argv[])
{
	vector<wstring> files;
	//wstring path = ExePath();
	wstring path2 = ExePath();
	//path = L"C:\\Users\\CC\\Documents\\shuame";
	//path = L"c:\\Users\\CC\\documents\\visual studio 2017\\Projects\\current_path\\current_path";
	//path2 = L"C:\\Users\\CC\\Documents\\shuame\\bbb";
	wofstream myfile;
	myfile.open("path.txt");

	//locale &loc = locale::global(locale(locale(), "", LC_CTYPE));  // 不论以输出文件流还是输入文件流，此操作应放在其两边 
	locale loc("chs");
	std::wcout.imbue(std::locale("chs"));
	myfile.imbue(std::locale("chs"));
	//wcout << L"中國" << endl;
	if (ListFiles(path2, L"*", files)) {
		for (vector<wstring>::iterator it = files.begin();
			it != files.end();
			++it) {
			wstring abc =  it->c_str();

			//string s(abc.begin(), abc.end());

			vector<wstring> result;
			split(abc, L'\\', result);

			wcout << result[result.size()-1] << endl;

			
			myfile << result[result.size() - 1] << endl;
			

			//wcout << it->c_str() << endl;
		}
	}
	myfile.close();
	//cout << "ENDED" << endl;
	system("pause");
	return 0;
}