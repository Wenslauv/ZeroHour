#pragma once

#include "CoreMinimal.h"
#include "GameFramework/CheatManager.h"
#include "ZhCheatManager.generated.h"

/**
 * Debug console commands for ZeroHour, available in the editor and development builds.
 */
UCLASS()
class ZEROHOUR_API UZhCheatManager : public UCheatManager
{
	GENERATED_BODY()
	
public:
	UFUNCTION(Exec)
	void ZhGiveAmmo();
};
