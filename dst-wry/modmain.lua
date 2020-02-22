PrefabFiles = {
	"WRY",
	"WRY_none",
}

Assets = {
    Asset( "IMAGE", "images/saveslot_portraits/WRY.tex" ),
    Asset( "ATLAS", "images/saveslot_portraits/WRY.xml" ),

    Asset( "IMAGE", "images/selectscreen_portraits/WRY.tex" ),
    Asset( "ATLAS", "images/selectscreen_portraits/WRY.xml" ),
	
    Asset( "IMAGE", "images/selectscreen_portraits/WRY_silho.tex" ),
    Asset( "ATLAS", "images/selectscreen_portraits/WRY_silho.xml" ),

    Asset( "IMAGE", "bigportraits/WRY.tex" ),
    Asset( "ATLAS", "bigportraits/WRY.xml" ),
	
	Asset( "IMAGE", "images/map_icons/WRY.tex" ),
	Asset( "ATLAS", "images/map_icons/WRY.xml" ),
	
	Asset( "IMAGE", "images/avatars/avatar_WRY.tex" ),
    Asset( "ATLAS", "images/avatars/avatar_WRY.xml" ),
	
	Asset( "IMAGE", "images/avatars/avatar_ghost_WRY.tex" ),
    Asset( "ATLAS", "images/avatars/avatar_ghost_WRY.xml" ),
	
	Asset( "IMAGE", "images/avatars/self_inspect_WRY.tex" ),
    Asset( "ATLAS", "images/avatars/self_inspect_WRY.xml" ),
	
	Asset( "IMAGE", "images/names_WRY.tex" ),
    Asset( "ATLAS", "images/names_WRY.xml" ),
	
	Asset( "IMAGE", "images/names_gold_WRY.tex" ),
    Asset( "ATLAS", "images/names_gold_WRY.xml" ),
}

AddMinimapAtlas("images/map_icons/WRY.xml")

local require = GLOBAL.require
local STRINGS = GLOBAL.STRINGS

-- The character select screen lines
STRINGS.CHARACTER_TITLES.WRY = "The Sample Character"
STRINGS.CHARACTER_NAMES.WRY = "Esc"
STRINGS.CHARACTER_DESCRIPTIONS.WRY = "*Perk 1\n*Perk 2\n*Perk 3"
STRINGS.CHARACTER_QUOTES.WRY = "\"Quote\""

-- Custom speech strings
STRINGS.CHARACTERS.WRY = require "speech_WRY"

-- The character's name as appears in-game 
STRINGS.NAMES.WRY = "Esc"
STRINGS.SKIN_NAMES.WRY_none = "Esc"

-- Add mod character to mod character list. Also specify a gender. Possible genders are MALE, FEMALE, ROBOT, NEUTRAL, and PLURAL.
AddModCharacter("WRY", "FEMALE")
