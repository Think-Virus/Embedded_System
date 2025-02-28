/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * File Name          : freertos.c
  * Description        : Code for freertos applications
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "FreeRTOS.h"
#include "task.h"
#include "main.h"
#include "cmsis_os.h"

#include "usart.h"
#include "adc.h"

osThreadId defaultTaskHandle;
osThreadId Tread1Handle;
osThreadId Tread2Handle;
osMutexId tx_mutexHandle;

typedef uint32_t ThreadProfiler_T;

ThreadProfiler_T DefaultThread_Profiler, Thread1_Profiler, Thread2_Profiler;

UART_HandleTypeDef huart2;

ADC_HandleTypeDef hadc1;
uint32_t sensorValues[4];

uint8_t buttonStatus;

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */

/* USER CODE END FunctionPrototypes */

void StartDefaultTask(void const * argument);
void Tread1Func(void const * argument);
void Tread2Func(void const * argument);

void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/* GetIdleTaskMemory prototype (linked to static allocation support) */
void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleTaskStackBuffer, uint32_t *pulIdleTaskStackSize );

/* USER CODE BEGIN GET_IDLE_TASK_MEMORY */
static StaticTask_t xIdleTaskTCBBuffer;
static StackType_t xIdleStack[configMINIMAL_STACK_SIZE];

void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleTaskStackBuffer, uint32_t *pulIdleTaskStackSize )
{
  *ppxIdleTaskTCBBuffer = &xIdleTaskTCBBuffer;
  *ppxIdleTaskStackBuffer = &xIdleStack[0];
  *pulIdleTaskStackSize = configMINIMAL_STACK_SIZE;
  /* place for user code */
}
/* USER CODE END GET_IDLE_TASK_MEMORY */

/**
  * @brief  FreeRTOS initialization
  * @param  None
  * @retval None
  */
void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */
	HAL_ADC_Start_DMA(&hadc1, sensorValues, 4);
  /* USER CODE END Init */
  /* Create the mutex(es) */
  /* definition and creation of tx_mutex */
  osMutexDef(tx_mutex);
  tx_mutexHandle = osMutexCreate(osMutex(tx_mutex));

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* definition and creation of defaultTask */
  osThreadDef(defaultTask, StartDefaultTask, osPriorityNormal, 0, 128);
  defaultTaskHandle = osThreadCreate(osThread(defaultTask), NULL);

  /* definition and creation of Tread1 */
  osThreadDef(Tread1, Tread1Func, osPriorityIdle, 0, 128);
  Tread1Handle = osThreadCreate(osThread(Tread1), NULL);

  /* definition and creation of Tread2 */
  osThreadDef(Tread2, Tread2Func, osPriorityIdle, 0, 128);
  Tread2Handle = osThreadCreate(osThread(Tread2), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */
}

/* USER CODE BEGIN Header_StartDefaultTask */
/**
  * @brief  Function implementing the defaultTask thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_StartDefaultTask */
void StartDefaultTask(void const * argument)
{
  /* USER CODE BEGIN StartDefaultTask */
  /* Infinite loop */
  for(;;)
  {
	  DefaultThread_Profiler++;
    osDelay(1);
  }
  /* USER CODE END StartDefaultTask */
}

/* USER CODE BEGIN Header_Tread1Func */
/**
* @brief Function implementing the Tread1 thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_Tread1Func */
void Tread1Func(void const * argument)
{
//	uint8_t message[30] = "Greeting from Thread 1 \r\n";
  for(;;)
  {
//	  Thread1_Profiler++;
//	  HAL_UART_Transmit(&huart2, message, 30, 1000);

//    osDelay(1);

//	  HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_6);
//	  osDelay(500);
	  uart_send_data('S', 1200);
	  osDelay(1);
  }
  /* USER CODE END Tread1Func */
}

/* USER CODE BEGIN Header_Tread2Func */
/**
* @brief Function implementing the Tread2 thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_Tread2Func */
void Tread2Func(void const * argument)
{
//	uint8_t message[30] = "Greeting from Thread 2 \r\n";
  /* USER CODE BEGIN Tread2Func */
  /* Infinite loop */
  for(;;)
  {
//	  Thread2_Profiler++;

//	  buttonStatus = HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13);
//	  HAL_UART_Transmit(&huart2, message, 30, 1000);
//    osDelay(1);

	  //HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_4);
	  HAL_GPIO_TogglePin(GPIOB, OUTPUT4_Pin);
	  osDelay(600);
  }
  /* USER CODE END Tread2Func */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */

/* USER CODE END Application */
