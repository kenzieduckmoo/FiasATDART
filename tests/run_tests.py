#!/usr/bin/env python3
"""Lua 5.1 behavior and native-UI mock tests. pip install lupa==2.8."""
from pathlib import Path
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
date=os.date;time=os.time;F={};SlashCmdList={};UISpecialFrames={}
NOW=1801767600
function GetServerTime() return NOW end
function UnitGUID() return 'Player-1' end
function UnitName() return 'Voidchicken' end
function GetNormalizedRealmName() return 'Garona' end
function GetRealmName() return 'Garona' end
function UnitClass() return 'Priest','PRIEST',5 end
function UnitRace() return 'Human','Human' end
function UnitFactionGroup() return 'Alliance' end
function UnitSex() return 3 end
function UnitLevel() return 82 end
function UnitXP() return 130 end
function UnitXPMax() return 1000 end
function GetXPExhaustion() return 1500 end
function GetMaxLevelForPlayerExpansion() return 90 end
function GetCurrentRegion() return 1 end
function GetBindLocation() return 'Dornogal' end
function GetRealZoneText() return 'Isle of Dorn' end
function GetSubZoneText() return 'Dornogal' end
function GetSpecialization() return 1 end
function GetSpecializationInfo() return 256,'Discipline',nil,1234,'HEALER' end
function GetAverageItemLevel() return 604.7,602.4 end
function UnitStat(_,i) return i*10,i*20 end
function UnitArmor() return 100,200 end
function UnitHealthMax() return 123456 end
function UnitPowerMax() return 100 end
function UnitPowerType() return 0,'MANA' end
function GetProfessions() return 1,2,nil,3 end
function GetProfessionInfo(i)
 if i==1 then return 'Tailoring',1,100,100,0,0,197 end
 if i==2 then return 'Enchanting',2,75,100,0,0,333 end
 return 'Fishing',3,10,100,0,0,356
end
function InCombatLockdown() return false end
C_TradeSkillUI={GetBaseProfessionInfo=function()return {professionID=197,professionName='Tailoring'}end,
 GetChildProfessionInfo=function()return {professionID=2883,professionName='Khaz Algar Tailoring',skillLevel=100,maxSkillLevel=100}end,
 GetChildProfessionInfos=function()return {{professionID=2539,professionName='Outland Tailoring',skillLevel=75,maxSkillLevel=75},{professionID=2540,professionName='Classic Tailoring',skillLevel=0,maxSkillLevel=300}}end,
 GetAllRecipeIDs=function()return {1,2}end,GetRecipeInfo=function(id)return {learned=id==1}end,
 IsTradeSkillLinked=function()return false end,IsTradeSkillGuild=function()return false end}
local headerCollapsed=true
C_Reputation={GetNumFactions=function()return headerCollapsed and 1 or 2 end,
 GetFactionDataByIndex=function(i)
  if i==1 then return {name='Outland',factionID=1,isHeader=true,isCollapsed=headerCollapsed}end
  return {name='Honor Hold',factionID=946,reaction=6,currentStanding=9500,currentReactionThreshold=9000,nextReactionThreshold=21000,isAccountWide=false}
 end,
 ExpandFactionHeader=function()headerCollapsed=false end,CollapseFactionHeader=function()headerCollapsed=true end}
C_Map={GetBestMapForUnit=function()return 2248 end,GetMapInfo=function(id)return {mapType=3,name=id==84 and 'Stormwind' or 'Nagrand'}end}
C_MountJournal={GetMountIDs=function()return {1,2}end,GetMountInfoByID=function(id)return 'Mount',1,2,false,false,1,true,false,false,false,id==1 end}
C_PetJournal={GetNumPets=function()return 2000,30 end}
RAID_CLASS_COLORS={PRIEST={r=1,g=1,b=1}}
C_Timer={After=function(_,fn)fn()end}
C_AddOns={IsAddOnLoaded=function()return false end}
''')
lua.execute(r'''
frameCount=0;frames={}
local methods={}
function methods:SetPoint(...) self.points=self.points or {};self.points[#self.points+1]={...} end
function methods:ClearAllPoints() self.points={} end
function methods:SetScript(event,fn)assert(self.kind~='FontString','FontStrings cannot have frame scripts');self.scripts[event]=fn end
function methods:GetScript(event) return self.scripts[event] end
function methods:SetSize(w,h) self.w=w;self.h=h end
function methods:SetWidth(w) self.w=w end
function methods:SetHeight(h) self.h=h end
function methods:GetWidth() return self.w or 990 end
function methods:GetHeight() return self.h or 500 end
function methods:SetAlpha(v) self.alpha=v end
function methods:GetAlpha() return self.alpha or 1 end
function methods:SetValue(v) self.value=v;if self.scripts.OnValueChanged then self.scripts.OnValueChanged(self,v) end end
function methods:GetValue() return self.value end
function methods:SetText(t) self.text=t end
function methods:GetText() return self.text or '' end
function methods:Show() local was=self.shown;self.shown=true;if not was and self.scripts.OnShow then self.scripts.OnShow(self) end end
function methods:Hide() self.shown=false;self.focus=false;for _,f in ipairs(frames)do if f.focus then local ancestor=f.parent;while ancestor do if ancestor==self then f.focus=false;break end;ancestor=ancestor.parent end end end end
function methods:IsShown() return self.shown end
function methods:SetShown(v) if v then self:Show() else self:Hide() end end
function methods:SetVerticalScroll(v) self.scroll=v end
function methods:GetVerticalScroll() return self.scroll or 0 end
function methods:SetChecked(v) self.checked=v end
function methods:GetChecked() return self.checked end
function methods:GetPoint() return 'CENTER',UIParent,'CENTER',0,0 end
setmetatable(methods,{__index=function(_,key) if key:match('^[A-Z]') then return function() end end end})
function CreateFrame(kind,name,parent,template)
 frameCount=frameCount+1
 local f=setmetatable({uid=frameCount,kind=kind,name=name,parent=parent,template=template,scripts={},shown=true},{__index=methods})
 frames[#frames+1]=f
 if name then _G[name]=f end
 return f
end
function methods:CreateFontString(_,_,font) return CreateFrame('FontString',nil,self,font) end
function methods:CreateTexture() return CreateFrame('Texture',nil,self) end
function methods:SetFrameLevel(v) self.level=v end
function methods:SetEnabled(v)self.enabled=v end
function methods:IsEnabled()return self.enabled~=false end
function methods:GetFrameLevel() return self.level or 3 end
function methods:GetEffectiveScale() return 1 end
function methods:GetCenter() return 100,100 end
UIParent=CreateFrame('Frame');UIParent:SetSize(1920,1080)
GameTooltip=CreateFrame('Frame')
function StaticPopup_Show(name,text,_,data) lastPopup={name=name,text=text,data=data} end

function methods:HasFocus() return self.focus==true end
function methods:SetFocus() self.focus=true end
function methods:GetLeft() return 300 end
function methods:GetTop() return 900 end
CURSOR_X=1220;CURSOR_Y=260
function GetCursorPosition() return CURSOR_X,CURSOR_Y end
function methods:ClearFocus() self.focus=false end
function methods:SetText(text) self.text=text;if self.scripts.OnTextChanged then self.scripts.OnTextChanged(self,false)end end
Minimap=CreateFrame('Frame');Minimap:SetSize(140,140)
''')
for filename in ['Core.lua','ATT.lua','UI.lua','Minimap.lua']:
    lua.execute("assert(loadfile(...))('FiammaCollector',F)",str(ROOT/filename))
lua.execute(r'''
F.Init();F.Current()
assert(F.db==FiammaCollectorDB and DuckMooFolioDB==nil,'Standalone addon touched Folio saved data')
local app,message=F.ATTStatus();assert(not app and message:find('Enable All The Things'))
F.Show();assert(F.frame:IsShown() and F.frame:GetWidth()==440)
assert(F.close:GetFrameLevel()>F.drag:GetFrameLevel(),'Drag frame covers close button')
F.close:GetScript('OnClick')(F.close);assert(not F.frame:IsShown());F.Show()
local opened=0
AllTheThings={ToggleMainList=function()opened=opened+1 end,Windows={}}
F.OpenATT();assert(opened==1,'Open ATT failed while the ATT tree was preparing')
local dungeon={instanceID=10,text='|cffff7d01Legacy Dungeon|r',total=10,progress=2,visible=true}
local raid={instanceID=11,text='Legacy Raid',total=100,progress=20,visible=true}
local root={modeString='Character mode',g={
 {tierID=2,headerID=100,g={dungeon}},
 {tierID=2,headerID=101,g={raid}},
 {mapID=107,g={{questID=1,collectible=true,visible=true},{questID=1,collectible=true,visible=true},{questID=2,collectible=true,collected=true}}},
 {tierID=1,mapID=84,g={{questID=3,collectible=true,visible=true}}},
 {tierID=11,headerID=101,g={{instanceID=12,text='War Within raid',total=10,progress=0,visible=true}}},
 {tierID=12,headerID=101,g={{instanceID=13,text='Midnight raid',total=10,progress=0,visible=true}}}
}}
local mainInstances={headerID=102,g={root.g[1],root.g[2],root.g[5],root.g[6]}}
root.g={mainInstances,root.g[3],root.g[4]}
AllTheThings={Windows={Prime={data=root}},HeaderConstants={DUNGEONS_AND_RAIDS=102,RAIDS=101,DUNGEONS=100},ToggleMainList=function()opened=opened+1 end,GroupFilter=function()return true end}
F.RefreshCurrent();local c=F.db.characters['Player-1'];local snapshot=c.att
assert(#snapshot.dungeons==1 and #snapshot.raids==1 and #snapshot.zones==1 and snapshot.zones[1].missing==1)
assert(snapshot.zones[1].expansion=='The Burning Crusade' and #snapshot.completion==2)
assert(snapshot.atdart and snapshot.atdart.progress/snapshot.atdart.total==.2)
local target=snapshot.atdart.instanceID
assert(dungeon.total==10 and dungeon.progress==2,'ATT live data changed')
F.Render();assert(#F.visibleRows.dungeons==1 and #F.visibleRows.raids==1 and #F.visibleRows.zones==1)
assert(F.pool[1].number:GetText()=='20.00%' and F.pool[1].name:GetText()=='ATDART % Target')
local function header(title)
 for _,r in ipairs(F.pool)do if r:IsShown() and r.toggle:IsShown() and r.toggle.caption:GetText():find(title,1,true)then return r end end
 error('Missing section '..title)
end
local h=F.frame:GetHeight();header('Legacy Dungeons').toggle:GetScript('OnClick')();assert(F.db.settings.collapsed.dungeons and F.frame:GetHeight()<h,'Collapse did not tighten the window')
header('Legacy Dungeons').toggle:GetScript('OnClick')();assert(not F.db.settings.collapsed.dungeons)
header('Legacy Dungeons').filter:GetScript('OnClick')();assert(F.chooser.options[1].id==false)
F.chooser.rows[2]:GetScript('OnClick')();assert(F.db.settings.filters.dungeons=='The Burning Crusade')
F.db.settings.filters.dungeons='Midnight';F.Render();assert(#F.visibleRows.dungeons==0 and #F.visibleRows.raids==1,'Section expansion filters are not independent')
F.db.settings.filters.dungeons=nil;F.Render()
-- Offline snapshots and refresh availability remain isolated per character.
F.db.characters.Alt={name='Alt',realm='Saurfang',att=F.Clean(snapshot)}
F.selected='Alt';F.Render();assert(not F.refresh:IsEnabled() and F.character.caption:GetText()=='Alt-Saurfang')
F.character:GetScript('OnClick')();F.chooser.rows[1]:GetScript('OnClick')();assert(F.selected=='Alt')
F.selected=F.current;F.Render();assert(F.refresh:IsEnabled())
local framesBefore=frameCount
for i=1,50 do F.Render()end
assert(frameCount==framesBefore,'Browsing leaked frames')
assert(c.att.atdart.instanceID==target,'Browsing rerolled target')
local before=c.att;InCombatLockdown=function()return true end;F.RefreshATT();assert(c.att==before and F.attMessage=='Refresh after combat.')
InCombatLockdown=function()return false end;F.attMessage=nil
-- Resize uses cursor deltas and begins without a jump.
local w,h=F.frame:GetWidth(),F.frame:GetHeight()
F.grip:GetScript('OnMouseDown')(F.grip,'LeftButton');F.grip:GetScript('OnUpdate')();assert(F.frame:GetWidth()==w and F.frame:GetHeight()==h)
CURSOR_X=CURSOR_X+40;CURSOR_Y=CURSOR_Y-20;F.grip:GetScript('OnUpdate')();assert(F.frame:GetWidth()==w+40 and F.frame:GetHeight()==h+20)
F.grip:GetScript('OnMouseUp')();assert(F.db.settings.width==w+40)
F.CreateMinimap();assert(F.minimap:IsShown());F.minimap:GetScript('OnClick')(F.minimap,'LeftButton');assert(not F.frame:IsShown())
F.minimap:GetScript('OnClick')(F.minimap,'LeftButton');assert(F.frame:IsShown())
SlashCmdList.FIAMMACOLLECTOR('minimap');assert(not F.minimap:IsShown())
SlashCmdList.FIAMMACOLLECTOR('');assert(F.frame:IsShown())
assert(SLASH_FIAMMACOLLECTOR1=='/fiamma' and SLASH_FIAMMACOLLECTOR2=='/atdart')
-- Saved snapshots and layout survive a simulated addon initialization.
local saved=F.Clean(FiammaCollectorDB);FiammaCollectorDB=saved;F.Init();assert(F.db.characters['Player-1'].att.atdart.instanceID==target)
assert(F.db.settings.width==w+40)
AllTheThings=nil;F.Render();assert(F.status:GetText():find('Enable All The Things') and #F.visibleRows.raids==1,'Offline cached data disappeared when ATT was unavailable')
print('PASS: standalone data isolation, ATT unavailable/loading states, opening ATT, legacy cutoff, read-only ranks, quest deduplication, target percentages/persistence, independent filters, collapse fitting, offline characters, close controls, stable frame reuse, combat deferral, resize, minimap and slash commands')
''')
lua.execute(r'''
-- Firelands screenshot regression: the main ATT row is 294/303 (9 missing),
-- while a different reference to the same instance has 10/193 (5.18%).
F.Current();F.selected=F.current;F.db.settings.filters={};F.db.settings.collapsed={}
InCombatLockdown=function()return false end
local firelands={instanceID=78,tierID=4,text='Firelands',total=303,progress=294,visible=true}
local alternate={instanceID=78,tierID=4,text='Firelands',total=193,progress=10,visible=true}
local nested={instanceID=78,tierID=4,text='Firelands difficulty reference',total=193,progress=10,visible=true}
firelands.g={nested}
local main={headerID=102,g={firelands}}
local reference={headerID=101,tierID=4,g={alternate}}
local dynamic={sourceIgnored=true,g={alternate,firelands}}
main.g[2]=dynamic
local root={modeString='Insane Account Completion Mode',g={main,reference}}
AllTheThings={Windows={Prime={data=root}},HeaderConstants={DUNGEONS_AND_RAIDS=102,RAIDS=101,DUNGEONS=100}}
EJ_GetCurrentTier=function()return 4 end;EJ_GetNumTiers=function()return 4 end
EJ_SelectTier=function()end
EJ_GetInstanceByIndex=function(i,raid)if i==1 and raid then return 78 end end
local function capture()
 F.RefreshCurrent();return F.db.characters[F.current].att
end
local snapshot=capture()
assert(snapshot.schema==4 and #snapshot.completion==1)
assert(snapshot.atdart.progress==294 and snapshot.atdart.total==303)
assert(snapshot.raids[1].missing==9 and string.format('%.2f',100*snapshot.atdart.progress/snapshot.atdart.total)=='97.03')
F.Render();assert(F.pool[1].number:GetText()=='97.03%','Native target label disagrees with main ATT counts')
-- Walking a reference first must not make the shared canonical object disappear.
root.g={reference,main};snapshot=capture();assert(snapshot.atdart.progress==294)
local other={instanceID=79,tierID=4,text='Another raid',total=100,progress=20,visible=true}
main.g[3]=other;AllTheThings.HeaderConstants.RAIDS=101;main.headerID=102
-- Preserve classification from ATT raid headers without an EJ match.
main.g[3]={headerID=101,g={other}}
snapshot=capture();assert(snapshot.atdart.instanceID==79,'Wrong Firelands reference still dominates ATDART')
assert(firelands.total==303 and firelands.progress==294 and alternate.progress==10,'Read-only capture changed ATT')
-- Conflicting canonical entries are omitted, rather than selecting whichever
-- happens to have the largest missing count or whichever was visited last.
main.g[4]={instanceID=78,tierID=4,total=193,progress=10,visible=true}
snapshot=capture();assert(snapshot.ambiguousInstances==1 and #snapshot.completion==1 and snapshot.atdart.instanceID==79)
-- Without the actual main category, do not fall back to arbitrary copies.
local prior=snapshot;root.g={reference};snapshot=capture();assert(snapshot==prior and F.attMessage,'Unavailable main data overwrote a valid snapshot')
-- Old saved wrong targets remain stored but are not shown as trustworthy data.
local old={schema=3,seenAt=NOW,mode='Old mode',completion={alternate},atdart=F.Clean(alternate),targetEvaluated=true,raids={alternate},dungeons={},zones={}}
F.db.characters[F.current].att=old;F.Render()
assert(F.GetATDART(old)==nil and F.pool[1].number:GetText()=='' and #F.visibleRows.raids==0)
assert(F.status:GetText():find('Refresh') and old.atdart.progress==10,'Old snapshot was deleted or silently treated as fixed')
-- Exact fractions and random ties remain stable within one validated capture.
local tied={schema=4,completion={{instanceID=1,tier=4,progress=1,total=3},{instanceID=2,tier=4,progress=2,total=6}}}
F.SelectATDART(tied,function(n)assert(n==2);return 2 end);assert(F.GetATDART(tied).instanceID==2)
print('PASS: Firelands 97.03% / 9 missing, alternate/nested/dynamic references, traversal order, ambiguous/missing canonical data, old-capture refresh requirement, exact ties and native percentage label')
''')
print('All tests passed. Actual Retail client verification is still required.')
