#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ZhProjectile.generated.h"

/**
 * Projectile fired by projectile weapons (and later by ranged enemies); deals radial damage on impact.
 */
UCLASS()
class ZEROHOUR_API AZhProjectile : public AActor
{
	GENERATED_BODY()

public:
	AZhProjectile();

protected:
	virtual void BeginPlay() override;
};
