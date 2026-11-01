#pragma once

#include "CoreMinimal.h"

#include "ZhAmmoType.generated.h"

/**
 * Ammo pools shared by weapons; the inventory keeps a count per type.
 */
UENUM(BlueprintType)
enum class EZhAmmoType : uint8
{
	Shells,
	
	Rockets,
};
