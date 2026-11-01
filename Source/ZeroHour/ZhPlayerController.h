#pragma once

#include "CoreMinimal.h"
#include "ZeroHourPlayerController.h"
#include "ZhPlayerController.generated.h"

/**
 * Player controller: adds the ZeroHour cheat manager on top of the template controller.
 */
UCLASS()
class ZEROHOUR_API AZhPlayerController : public AZeroHourPlayerController
{
	GENERATED_BODY()
	
	
public:
	AZhPlayerController();
};
