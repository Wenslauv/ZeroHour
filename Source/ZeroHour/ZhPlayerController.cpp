#include "ZhPlayerController.h"

#include "ZhCheatManager.h"

AZhPlayerController::AZhPlayerController()
{
	CheatClass = UZhCheatManager::StaticClass();
}
