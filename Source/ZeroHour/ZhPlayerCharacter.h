// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "ZeroHourCharacter.h"
#include "ZhPlayerCharacter.generated.h"


class UInputAction;

UCLASS()
class ZEROHOUR_API AZhPlayerCharacter : public AZeroHourCharacter
{
	GENERATED_BODY()

public:
	AZhPlayerCharacter();

protected:
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	
protected:
	UPROPERTY(EditDefaultsOnly, Category = "Input|Combat")
	TObjectPtr<UInputAction> FireAction;
	UPROPERTY(EditDefaultsOnly, Category = "Input|Combat")
	TObjectPtr<UInputAction> NextWeaponAction;
	UPROPERTY(EditDefaultsOnly, Category = "Input|Combat")
	TObjectPtr<UInputAction> PrevWeaponAction;
	UPROPERTY(EditDefaultsOnly, Category = "Input|Combat")
	TObjectPtr<UInputAction> Weapon1Action;
	UPROPERTY(EditDefaultsOnly, Category = "Input|Combat")
	TObjectPtr<UInputAction> Weapon2Action;
	UPROPERTY(EditDefaultsOnly, Category = "Input|Combat")
	TObjectPtr<UInputAction> InteractAction;
	
private:
	void Fire();
	void NextWeapon();
	void PrevWeapon();
	void SelectWeapon1();
	void SelectWeapon2();
	void Interact();
};
