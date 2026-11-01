#pragma once

#include "CoreMinimal.h"
#include "ZhAmmoType.h"
#include "Engine/DataAsset.h"
#include "ZhWeaponData.generated.h"

class AZhWeaponBase;
class AZhProjectile;

/**
 * Balance parameters of a weapon type: damage, fire rate, spread, ammo.
 * Visuals (mesh, sounds, effects) live in the weapon Blueprint.
 */
UCLASS()
class ZEROHOUR_API UZhWeaponData : public UPrimaryDataAsset
{
	GENERATED_BODY()
	
public:
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon")
	FText DisplayName;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon")
	TSubclassOf<AZhWeaponBase> WeaponClass;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Fire", meta=(ClampMin="0"))
	float ShotsPerSecond = 1.0f;	
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Fire", meta=(ClampMin="1"))
	int32 ProjectilesPerShot = 1;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Fire", meta=(ClampMin="0", Units="Degrees"))
	float SpreadAngle = 0;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Fire", meta=(ClampMin="0", Units="cm"))
	float Range = 3000.0f;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Ammo")
	EZhAmmoType AmmoType = EZhAmmoType::Shells;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Ammo", meta=(ClampMin="1"))
	int32 AmmoPerShoot = 1;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Ammo")
	TSubclassOf<AZhProjectile> ProjectileClass;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Damage", meta=(ClampMin="0"))
	float Damage = 1.0f;
	
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Weapon|Damage", meta=(ClampMin="0", Units="cm"))
	float ExplosionRadius = 0.0f;
};
