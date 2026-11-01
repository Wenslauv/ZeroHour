#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ZhWeaponBase.generated.h"

/**
 * Base weapon actor: fire cooldown and aiming. Subclasses implement the shot itself.
 * Ammo is owned by the inventory; the weapon only knows how to fire.
 */
UCLASS(Abstract)
class ZEROHOUR_API AZhWeaponBase : public AActor
{
	GENERATED_BODY()

public:
	AZhWeaponBase();

protected:
	virtual void BeginPlay() override;
};
