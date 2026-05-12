#include "protocol-task.h"
#include "stdio.h"
#include "stdlib.h"
#include "pico/stdlib.h"
#include "string.h"
#include "stdint.h"
static api_t* api = {0};
static int commands_count = 0;

// инициализация
void protocol_task_init(api_t* commands_array)
{
    // Сохраняем указатель на массив команд
    api = commands_array;
    
    // Подсчитываем число команд
    commands_count = 0;
    
    if (api != NULL)
    {
        // Проходим по массиву, пока не встретим элемент с command_name == NULL
        while (api[commands_count].command_name != NULL)
        {
            commands_count++;
        }
    }
}

// Функция обработки команды
void protocol_task_handle(char* command_string)
{
    if (!command_string)
    {
        return;
    }
    const char* command_name = command_string;
    const char* command_args = NULL;
// strchr ищет первое вхождение пробела в строке sentence и выводит позицию этого символа
    char* space_symbol = strchr(command_string, ' ');
    if (space_symbol)
    {
        *space_symbol = '\0';
        command_args = space_symbol + 1;
    }
    else
    {
        command_args = "";
    }
    // Вывод найденных имени команды и ее аргументов
    printf("Command: '%s', Args: '%s'\n", command_name, command_args);
    // Проверка на совпадение имен команд в массиве
    for (int i = 0; i < commands_count; i++){
        if (strcmp(command_name, api[i].command_name) != 0){
            continue; // продолжаем поиск совпадений
        }
        api[i].command_callback(command_args);
        return;
    }
    // Команда не найдена
    printf("Unknown command: '%s'\n", command_name);
    return;
}
void mem_prot(uint32_t addr){
    uint32_t value = *(uint32_t*)addr;
    printf("Value at 0x%08X: 0x%08X\n", addr, value);
}


void wmem_prot(uint32_t addr, uint32_t value){
    *(uint32_t*)addr = value;
    printf("Written 0x%08X to address 0x%08X\n", value, addr);
}