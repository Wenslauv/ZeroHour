#include "ZhPlayerCharacter.h"
#include "EnhancedInputComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "ZeroHour.h"

AZhPlayerCharacter::AZhPlayerCharacter()
{
	UCharacterMovementComponent* Movement = GetCharacterMovement();
	Movement->MaxWalkSpeed = 1500.f;
	Movement->MaxAcceleration = 4096.f;
	Movement->BrakingDecelerationWalking = 4096.f;
	Movement->GroundFriction = 8.f;
	Movement->AirControl = 0.5f;
	Movement->JumpZVelocity = 900.f;
	Movement->GetNavAgentPropertiesRef().bCanCrouch = false;
}

void AZhPlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
	
	UEnhancedInputComponent* Input = CastChecked<UEnhancedInputComponent>(PlayerInputComponent);
	auto Bind = [this, Input](UInputAction* Action, void (AZhPlayerCharacter::*Handler)())
	{
		if (ensureMsgf(Action, TEXT("Input action is not set on %s"), *GetName()))
		{
			Input->BindAction(Action, ETriggerEvent::Started, this, Handler);
		}
	};
	Bind(FireAction, &AZhPlayerCharacter::Fire);
	Bind(NextWeaponAction, &AZhPlayerCharacter::NextWeapon);
	Bind(PrevWeaponAction, &AZhPlayerCharacter::PrevWeapon);
	Bind(Weapon1Action, &AZhPlayerCharacter::SelectWeapon1);
	Bind(Weapon2Action, &AZhPlayerCharacter::SelectWeapon2);
	Bind(InteractAction, &AZhPlayerCharacter::Interact);
}

// Stubbed methods for next iterations
void AZhPlayerCharacter::Fire()				{ UE_LOG(LogZeroHour, Log, TEXT("Fire")); }
void AZhPlayerCharacter::NextWeapon()		{ UE_LOG(LogZeroHour, Log, TEXT("Next weapon")); }
void AZhPlayerCharacter::PrevWeapon()		{ UE_LOG(LogZeroHour, Log, TEXT("Prev weapon")); }
void AZhPlayerCharacter::SelectWeapon1()	{ UE_LOG(LogZeroHour, Log, TEXT("Weapon 1")); }
void AZhPlayerCharacter::SelectWeapon2()	{ UE_LOG(LogZeroHour, Log, TEXT("Weapon 2")); }
void AZhPlayerCharacter::Interact()			{ UE_LOG(LogZeroHour, Log, TEXT("Interact")); }
