local addon,F=...
F.name=addon;F.version='0.1.2';F.Model={}
local M=F.Model
function F.Safe(fn,...)
    if type(fn)~='function' then return nil end
    local function pack(...) return {n=select('#',...),...} end
    local results=pack(pcall(fn,...))
    if not results[1] then return nil end
    for i=2,results.n do if issecretvalue and issecretvalue(results[i]) then results[i]=nil end end
    return unpack(results,2,results.n)
end
local S=F.Safe
function F.Clean(value,depth)
    if issecretvalue and issecretvalue(value) then return nil end
    local kind=type(value)
    if kind=='number' or kind=='string' or kind=='boolean' then return value end
    if kind=='table' and (depth or 0)<8 then
        local out={}
        for k,v in pairs(value) do
            if not (issecretvalue and issecretvalue(k)) and (type(k)=='string' or type(k)=='number') then out[k]=F.Clean(v,(depth or 0)+1) end
        end
        return out
    end
end

function M.Plain(s)return tostring(s or ''):gsub('|','||')end
function M.Display(s)
    return tostring(s or ''):gsub('|c[fF][fF][fF][fF][fF]7[dD]01',''):gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r',''):gsub('|H.-|h(.-)|h','%1'):gsub('|T.-|t',''):gsub('|A.-|a','')
end

function F.Now()return F.Safe(GetServerTime) or time()end
function F.Init()
    FiammaCollectorDB=FiammaCollectorDB or {}
    F.db=FiammaCollectorDB;F.db.characters=F.db.characters or {};F.db.settings=F.db.settings or {}
    local settings=F.db.settings;settings.collapsed=settings.collapsed or {};settings.filters=settings.filters or {}
end
function F.Current()
    if not F.db then return end
    local guid=F.Safe(UnitGUID,'player');if not guid then return end
    local c=F.db.characters[guid] or {};F.db.characters[guid]=c
    c.name=F.Safe(UnitName,'player') or c.name
    c.realm=F.Safe(GetRealmName) or c.realm
    F.current=guid;return c
end
function F.DrawIfShown()
    if F.frame and F.frame:IsShown() and not F.rendering then F.Render()end
end
function F.RefreshCurrent()
    F.Current();F.selected=F.current;F.RefreshATT()
end
local events=CreateFrame('Frame');F.events=events
for _,event in ipairs({'ADDON_LOADED','PLAYER_LOGIN','PLAYER_ENTERING_WORLD'})do events:RegisterEvent(event)end
events:SetScript('OnEvent',function(_,event,arg)
    if event=='ADDON_LOADED' then if arg==addon then F.Init()end;return end
    if not F.db then return end
    F.Current();if event=='PLAYER_LOGIN' then F.CreateMinimap()end
end)
SLASH_FIAMMACOLLECTOR1='/fiamma';SLASH_FIAMMACOLLECTOR2='/atdart'
SlashCmdList.FIAMMACOLLECTOR=function(command)
    if not F.db then F.Init()end;F.Current()
    command=(command or ''):lower():match('^%s*(.-)%s*$')
    if command=='minimap' then F.db.settings.hideMinimap=not F.db.settings.hideMinimap;F.CreateMinimap()
    elseif command=='refresh' then F.Show(true);F.RefreshCurrent()
    else F.Show()end
end
