// Fill out your copyright notice in the Description page of Project Settings.


#include "ZhPlayerController.h"

#include "ZhCheatManager.h"

AZhPlayerController::AZhPlayerController()
{
	CheatClass = UZhCheatManager::StaticClass();
}
