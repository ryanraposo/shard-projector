import re

src = """return {
  ["workshop-1378549454"]={
    configuration_options={
      ["MemSpikeFix:"]=false,
      MemSpikeFixmaster_override=true,
      ["MemSpikeFixworkshop-1207269058"]="default",
      ["MemSpikeFixworkshop-1467200656"]="default",
      ["MemSpikeFixworkshop-1467214795"]="default",
      ["MemSpikeFixworkshop-1505270912"]="default",
      ["MemSpikeFixworkshop-1643169967"]="default",
      ["MemSpikeFixworkshop-1780226102"]="default",
      ["MemSpikeFixworkshop-1836974133"]="default",
      ["MemSpikeFixworkshop-1849561588"]="default",
      ["MemSpikeFixworkshop-1918927570"]="default",
      ["MemSpikeFixworkshop-1938752683"]="default",
      ["MemSpikeFixworkshop-1953572884"]="default",
      ["MemSpikeFixworkshop-345692228"]="default",
      ["MemSpikeFixworkshop-350811795"]="default",
      ["MemSpikeFixworkshop-351325790"]="default",
      ["MemSpikeFixworkshop-352373173"]="default",
      ["MemSpikeFixworkshop-376333686"]="default",
      ["MemSpikeFixworkshop-378160973"]="default",
      ["MemSpikeFixworkshop-457415515"]="default",
      ["MemSpikeFixworkshop-531060374"]="default",
      ["MemSpikeFixworkshop-550937680"]="default",
      ["MemSpikeFixworkshop-618785273"]="default",
      ["MemSpikeFixworkshop-697356989"]="default",
      ["MemSpikeFixworkshop-791838548"]="default" 
    },
    enabled=true 
  },
  ["workshop-1467200656"]={ configuration_options={  }, enabled=true },
  ["workshop-1467214795"]={
    configuration_options={
      ["Misc."]=false,
      ["Tweaks & Changes"]=false,
      allowprimeapebarrel=true,
      autodisembark=false,
      bossbalance=true,
      devmode=false,
      droplootground=true,
      dynamicmusic=true,
      limestonerepair=true,
      locale=false,
      newplayerboats=false,
      oldwarly=false,
      scale_floodpuddles=0.01,
      tuningmodifiers=true 
    },
    enabled=true 
  },
  ["workshop-1780226102"]={
    configuration_options={
      AltEndtable=true,
      AltFloralshirt=false,
      AltHoundius=false,
      AltSeawreath=false,
      Contents=false,
      Glommer=0,
      Islands=false,
      Walrus=0,
      beequeen=true,
      dragonfly=2,
      moon1=true,
      oasis=true,
      sinkhole=true,
      volcano=false 
    },
    enabled=true 
  },
  ["workshop-1953572884"]={
    configuration_options={ commandstayfollow=118, nandodistance=0, nandoinstakill=1 },
    enabled=true 
  },
  ["workshop-350811795"]={ configuration_options={  }, enabled=true },
  ["workshop-697356989"]={
    configuration_options={
      classic_skin=false,
      enable_legacywarly=false,
      pondsurfer=true,
      surf_sanity="n",
      walani_drying=0.3,
      walani_sanity=0.9,
      wilburrun="y",
      woodlegs_luck=6,
      woodlegs_sanity=-0.08 
    },
    enabled=true 
  } 
}"""

# Finds all matches that begin with 'workshop-' followed by a seq of numbers 4 or more digits long
x = re.findall(r'workshop-[0-9]{4,}', src)
# But it would suffice to use...
mods = re.findall(r'"workshop-[0-9]+', src)
# ...which gets all of the same but only requires 1 or more digit sequences, denoted with the '+', vs the '{4,}'
print(mods) 

# This will find matches between 'configuration_options = {' and '}' 
configurations = re.findall(r'(?s)(?<=configuration_options={).*?(?=})', src)

x = 0
for each in configurations:
    # print(x, each)
    x+=1

mods_with_configs_dict = dict(zip(mods, configurations))

for k,v in mods_with_configs_dict.items():
    print('%s : %s'%(k,v))