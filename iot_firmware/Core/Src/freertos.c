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


void Tread1Func(void const * argument)
{
  for(;;)
  {
	  Thread1_Profiler++;
	  xSemaphoreTake(tx_mutexHandle, portMAX_DELAY);

	  // Test 1
	  uart_outchar('A');
	  uart_outdec(sensorValues[0]); // Temperature sensor at PA4 (ADC1_IN4)
	  uart_outcrfl();

	  uart_outchar('B');
	  uart_outdec(sensorValues[1]); // Pressure sensor at PA5 (ADC1_IN5)
	  uart_outcrfl();

	  uart_outchar('C');
	  uart_outdec(sensorValues[2]); // Battery 1 at PA6 (ADC1_IN6)
	  uart_outcrfl();

	  uart_outchar('D');
	  uart_outdec(sensorValues[3]); // Battery 2 at PA7 (ADC1_IN7)
	  uart_outcrfl();


	  xSemaphoreGive(tx_mutexHandle);

	  osDelay(1);
  }
}

uint8_t recv[2]; // Receiving data

void Tread2Func(void const * argument)
{

  for(;;)
  {
	  Thread2_Profiler++;

	  xSemaphoreTake(tx_mutexHandle, portMAX_DELAY);

	  HAL_UART_Receive(&huart2, recv, 4, 1000);

	  if (recv[0] == 65 && recv[1] == 49)
	  {
		  HAL_GPIO_WritePin(OUTPUT1_GPIO_Port, OUTPUT1_Pin, GPIO_PIN_SET);
	  }
	  else if (recv[0] == 65)
	  {
		  HAL_GPIO_WritePin(OUTPUT1_GPIO_Port, OUTPUT1_Pin, GPIO_PIN_RESET);
	  }

	  if (recv[0] == 66 && recv[1] == 49)
	  	  {
	  		  HAL_GPIO_WritePin(OUTPUT2_GPIO_Port, OUTPUT2_Pin, GPIO_PIN_SET);
	  	  }
	  else if(recv[0] == 66)
	  {
		  HAL_GPIO_WritePin(OUTPUT2_GPIO_Port, OUTPUT2_Pin, GPIO_PIN_RESET);
	  }

	  xSemaphoreGive(tx_mutexHandle);

	  buttonStatus = HAL_GPIO_ReadPin(BTN1_GPIO_Port, BTN1_Pin);

	  osDelay(1);

  }
}
