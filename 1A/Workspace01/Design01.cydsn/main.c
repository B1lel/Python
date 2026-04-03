#include <project.h>
#include <stdio.h>

int main()
{
    char message[80];
    CyGlobalIntEnable; 
    
    // Démarrage
    Timer_1_Start();
    Timer_2_Start();
    UART_1_Start();
    UART_2_Start();
    

    for(;;)
    {
        

        Timer_1_WriteCounter(16777215);
        Timer_2_WriteCounter(16777215);
        
        trigger_Write(1);
        CyDelayUs(10);                                    
        trigger_Write(0);
        
        CyDelay(50); 
        
        uint32 valeur_lue = Timer_1_ReadCounter();
        uint32 ticks_ecoules = 16777215 - valeur_lue;
        
        uint32 microsecondes = ticks_ecoules / 24;
        int dist = (int)(microsecondes / 58);
        
        // d'affichage
        if (dist >= 1 && dist <= 50) {
            sprintf(message, "distance : %d cm (Ticks: %lu)\r\n", dist, ticks_ecoules);
        } else {
            sprintf(message, "Distance : --- cm (Hors portee)\r\n");
        }
        UART_1_PutString(message);
        
        // Signal laser 
        if (dist >= 1 && dist <= 30) {
            sprintf(message,"1\n");
        } else {
            sprintf(message, "0\n");
        }
        UART_1_PutString(message); 
        UART_2_PutString(message); 
        
        // Temp boucle
        // uint32 time_ms = 16777215 - Timer_2_ReadCounter();
        //sprintf(message, "[%lu ms] Distance : %d cm\r\n", time_ms, dist);
        
    }
}