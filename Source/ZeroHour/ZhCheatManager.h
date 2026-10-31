// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/CheatManager.h"
#include "ZhCheatManager.generated.h"


UCLASS()
class ZEROHOUR_API UZhCheatManager : public UCheatManager
{
	GENERATED_BODY()
	
public:
	UFUNCTION(Exec)
	void ZhGiveAmmo();
};
