#include <windows.h>
#include <tlhelp32.h>
#include <iostream>

DWORD GetProcessId(const char *processName) {

    HANDLE hSnapshot = CreateToolhelp32Snapshot(
        TH32CS_SNAPPROCESS,
        0
    );
    if (hSnapshot) {
        PROCESSENTRY32 entry;
        entry.dwSize = sizeof(PROCESSENTRY32);
        if (Process32First(hSnapshot, &entry)) {
            do {
                if (!strcmp(entry.szExeFile, processName)) { return entry.th32ProcessID; }
            } while (Process32Next(hSnapshot, &entry));
        } 
    }
    return 0;
}

DWORD_PTR GetModuleBaseAddress(DWORD dwProcessId, const char* moduleName) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, dwProcessId);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }

    MODULEENTRY32 moduleEntry;
    moduleEntry.dwSize = sizeof(MODULEENTRY32);

    if (Module32First(hSnapshot, &moduleEntry)) {
        do {
            if (_stricmp(moduleEntry.szModule, moduleName) == 0) {
                CloseHandle(hSnapshot);
                return reinterpret_cast<DWORD_PTR>(moduleEntry.modBaseAddr);
            }
        } while (Module32Next(hSnapshot, &moduleEntry));
    }

    CloseHandle(hSnapshot);
    return 0;
}

void LogVirtualProtect(BOOL VPResult ) {
    if (VPResult) {
        std::cout << "VirtualProtect succeeded." << std::endl;
    } else {
        std::cerr << "VirtualProtectEx failed. Error code: " << GetLastError() << std::endl;
    }
}

int main() {
    
    const char* processName = "HackTheBox CubeMadness1.exe";
    const char* dllName = "GameAssembly.dll";
    
    DWORD processId = GetProcessId(processName);

    if (processId != 0) {
        DWORD_PTR baseAddress = GetModuleBaseAddress(processId, dllName);
        
        

        if (baseAddress != 0) {
            
            std::cout << "Base Address of " << dllName << " in " << processName << ": " << std::hex << baseAddress << std::endl;
            DWORD_PTR targetAddress = baseAddress + 0xA67119;
            
            std::cout << "Target address is " << std::hex << targetAddress << std::endl;
            HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);
            
            BYTE opcodes[] = { 0x48, 0x81, 0x00, 0xE7, 0x03, 0x00, 0x00 }; // { 0x48, 0xC7, 0x00, 0xE7, 0x03, 0x00, 0x00 }
            
            DWORD oldProtect = 0;
            BOOL VPResult = VirtualProtectEx(hProcess, reinterpret_cast<LPVOID>(targetAddress), sizeof(opcodes), PAGE_EXECUTE_READWRITE, &oldProtect);
            LogVirtualProtect(VPResult);
            
            if (VPResult) {
                
                WriteProcessMemory(hProcess, reinterpret_cast<LPVOID>(targetAddress), opcodes, sizeof(opcodes), NULL);
                std::cout << "OPCODE 'add [rax], 3E7' injected to target address" << std::endl;
                
                DWORD newProtect = 0;
                VPResult = VirtualProtectEx(hProcess, reinterpret_cast<LPVOID>(targetAddress), sizeof(opcodes), oldProtect, &newProtect);
                LogVirtualProtect(VPResult);
                std::cout << "Previous memory access restored. GO GRAB THAT CUBE!" << std::endl;
            }

        } else {
            std::cout << "DLL " << dllName << " not found in the process." << std::endl;
        }
    } else {
        std::cout << "Process "<< processName << " not found. Is the game running?" << std::endl;
    }
    
    return 0;
}