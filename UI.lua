local _,F=...
local M=F.Model
local white={1,1,1};local yellow={1,.87,.32};local muted={.82,.79,.87}
local function surface(kind,parent,r,g,b)
    local f=CreateFrame(kind,nil,parent,'BackdropTemplate')
    f:SetBackdrop({bgFile='Interface/Buttons/WHITE8X8',edgeFile='Interface/Buttons/WHITE8X8',edgeSize=1})
    f:SetBackdropColor(r or .065,g or .055,b or .08,1);f:SetBackdropBorderColor(.21,.13,.29,1)
    return f
end
local function label(parent,text,width,color,font)
    local f=parent:CreateFontString(nil,'OVERLAY',font or 'GameFontHighlightSmall');f:SetText(text);f:SetWidth(width);f:SetJustifyH('LEFT');f:SetWordWrap(false)
    local c=color or white;f:SetTextColor(c[1],c[2],c[3]);return f
end
local function button(parent,text,width,action)
    local b=surface('Button',parent,.12,.065,.18);b:SetSize(width,22);b:EnableMouse(true);b:RegisterForClicks('LeftButtonUp')
    b.caption=label(b,text,width-8);b.caption:SetPoint('CENTER');b.caption:SetJustifyH('CENTER')
    b:SetScript('OnClick',action)
    b:SetScript('OnEnter',function(self)self:SetBackdropColor(.20,.10,.28,1)end)
    b:SetScript('OnLeave',function(self)self:SetBackdropColor(.12,.065,.18,1)end)
    return b
end
local function tooltip(frame,title,lines)
    frame:SetScript('OnEnter',function(self)
        if self.caption then self:SetBackdropColor(.20,.10,.28,1)end
        GameTooltip:SetOwner(self,'ANCHOR_RIGHT');GameTooltip:SetText(title)
        for _,line in ipairs(lines)do GameTooltip:AddLine(line,1,1,1,true)end;GameTooltip:Show()
    end)
    frame:SetScript('OnLeave',function(self)if self.caption then self:SetBackdropColor(.12,.065,.18,1)end;GameTooltip:Hide()end)
end
function F.Choose(title,options,callback)
    local p=F.chooser
    if not p then
        p=surface('Frame',UIParent,.025,.02,.03);F.chooser=p;p:SetSize(304,346);p:SetPoint('CENTER');p:SetFrameStrata('DIALOG');p:EnableMouse(true)
        _G.FiammaCollectorChooser=p;table.insert(UISpecialFrames,'FiammaCollectorChooser')
        p.title=label(p,'',262,white,'GameFontNormal');p.title:SetPoint('TOPLEFT',6,-6)
        local close=button(p,'X',22,function()p:Hide()end);close:SetPoint('TOPRIGHT',-3,-3)
        p.rows={};for i=1,12 do
            local index=i;p.rows[i]=button(p,'',292,function()
                local choice=p.options[(p.page-1)*12+index];if choice then p:Hide();p.callback(choice.id)end
            end);p.rows[i]:SetPoint('TOPLEFT',6,-28-(i-1)*24)
        end
        local prev=button(p,'<',26,function()p.page=math.max(1,p.page-1);p.draw()end);prev:SetPoint('BOTTOMLEFT',6,4)
        local next=button(p,'>',26,function()p.page=p.page+1;p.draw()end);next:SetPoint('BOTTOMRIGHT',-6,4)
        p.counter=label(p,'',230,muted);p.counter:SetPoint('BOTTOMLEFT',40,9)
        p.draw=function()
            local pages=math.max(1,math.ceil(#p.options/12));p.page=math.min(p.page,pages)
            for i,b in ipairs(p.rows)do
                local option=p.options[(p.page-1)*12+i];b:SetShown(option~=nil);if option then b.caption:SetText(M.Plain(option.name))end
            end
            p.counter:SetText('Page '..p.page..' / '..pages)
        end
    end
    p.options=options;p.callback=callback;p.page=1;p.title:SetText(title);p:Show();p.draw()
end
function F.CreateWindow()
    if F.frame then return end
    local f=surface('Frame',UIParent,.018,.015,.024);F.frame=f
    _G.FiammaCollectorWindow=f;table.insert(UISpecialFrames,'FiammaCollectorWindow')
    f:SetSize(F.db.settings.width or 440,F.db.settings.height or 520);f:SetPoint('CENTER');f:SetFrameStrata('HIGH');f:SetClampedToScreen(true);f:EnableMouse(true);f:SetMovable(true);f:SetResizable(true)
    if f.SetResizeBounds then f:SetResizeBounds(360,170,1000,1100)end
    local p=F.db.settings.position;if p then f:ClearAllPoints();f:SetPoint(p[1],UIParent,p[2],p[3],p[4])end
    local drag=CreateFrame('Frame',nil,f);F.drag=drag;drag:SetPoint('TOPLEFT');drag:SetPoint('TOPRIGHT');drag:SetHeight(31);drag:SetFrameLevel(f:GetFrameLevel()+1);drag:EnableMouse(true);drag:RegisterForDrag('LeftButton')
    drag:SetScript('OnDragStart',function()f:StartMoving()end)
    drag:SetScript('OnDragStop',function()f:StopMovingOrSizing();local a,_,b,x,y=f:GetPoint();F.db.settings.position={a,b,x,y}end)
    local title=label(f,"FIAMMA'S COLLECTOR",370,white,'GameFontNormal');title:SetPoint('TOPLEFT',6,-9)
    local close=button(f,'X',22,function()f:Hide();if F.chooser then F.chooser:Hide()end end);F.close=close;close:SetPoint('TOPRIGHT',-3,-3);close:SetFrameLevel(drag:GetFrameLevel()+5)
    F.character=button(f,'Current character',180,function()
        local options={};for guid,c in pairs(F.db.characters)do options[#options+1]={id=guid,name=(c.name or '?')..'-'..(c.realm or '?')}end
        table.sort(options,function(a,b)return a.name<b.name end)
        F.Choose('Character snapshots',options,function(id)F.selected=id;F.scroll:SetVerticalScroll(0);F.Render()end)
    end)
    F.character:SetPoint('TOPLEFT',4,-33)
    F.open=button(f,'Open ATT',78,F.OpenATT)
    F.refresh=button(f,'Refresh',68,F.RefreshCurrent)
    F.help=button(f,'?',20,function()end)
    tooltip(F.help,'Fiamma Collector | DuckMoo Services',{'Made for Fiamma. /fiamma or /atdart opens this window.','ATDART shows the lowest legacy completion. Ties are picked once per capture.','Other lists rank missing collectibles or unfinished quests. Expand/collapse each section and filter by expansion.','Click a quest zone for counted IDs and an ATT zone window. /atdart debug on adds deeper diagnostics on the next Refresh.','Legacy stops at Dragonflight. The War Within and Midnight are excluded from legacy instance rankings.','Counts follow the captured ATT profile and availability filters, not drop chances. Offline characters show saved snapshots.','All timestamps use your local time. Resize at the bottom-right; drag the title to move.'})
    F.status=label(f,'',420,muted);F.status:SetPoint('TOPLEFT',5,-61);F.status:SetHeight(16)
    F.scroll=CreateFrame('ScrollFrame',nil,f,'UIPanelScrollFrameTemplate');F.scroll:SetPoint('TOPLEFT',4,-82);F.scroll:SetPoint('BOTTOMRIGHT',-22,5)
    F.body=CreateFrame('Frame',nil,F.scroll);F.body:SetPoint('TOPLEFT',F.scroll,'TOPLEFT');F.scroll:SetScrollChild(F.body)
    F.pool={};F.used=0
    local grip=CreateFrame('Button',nil,f);F.grip=grip;grip:SetSize(16,16);grip:SetPoint('BOTTOMRIGHT',-1,1);grip:SetNormalTexture('Interface/ChatFrame/UI-ChatIM-SizeGrabber-Up')
    grip:SetScript('OnMouseDown',function(_,mouse)
        if mouse~='LeftButton' then return end
        local x,y=GetCursorPosition();local scale=f:GetEffectiveScale();F.resizing={x=x/scale,y=y/scale,w=f:GetWidth(),h=f:GetHeight()}
        local left,top=f:GetLeft(),f:GetTop();if left and top then f:ClearAllPoints();f:SetPoint('TOPLEFT',UIParent,'BOTTOMLEFT',left,top)end
        grip:SetScript('OnUpdate',function()
            local mx,my=GetCursorPosition();local r=F.resizing
            f:SetSize(math.max(360,math.min(UIParent:GetWidth()-20,r.w+mx/scale-r.x)),math.max(170,math.min(UIParent:GetHeight()-20,r.h+r.y-my/scale)))
        end)
    end)
    grip:SetScript('OnMouseUp',function()
        grip:SetScript('OnUpdate',nil);F.resizing=nil;F.db.settings.width=f:GetWidth();F.db.settings.height=f:GetHeight()
        local a,_,b,x,y=f:GetPoint();F.db.settings.position={a,b,x,y};F.Render()
    end)
    f:SetScript('OnSizeChanged',function()if not F.rendering and not F.resizing then F.Render()end end)
    f:Hide()
end
local function row(y,height)
    F.used=F.used+1;local r=F.pool[F.used]
    if not r then
        r=surface('Frame',F.body);F.pool[F.used]=r;r:EnableMouse(true)
        r.name=label(r,'',260);r.name:SetPoint('TOPLEFT',5,-5)
        r.number=label(r,'',80,yellow);r.number:SetJustifyH('RIGHT');r.number:SetPoint('TOPRIGHT',-5,-5)
        r.detail=label(r,'',330,muted);r.detail:SetPoint('TOPLEFT',5,-24)
        r.toggle=button(r,'',220,function()end);r.toggle:SetPoint('TOPLEFT');r.filter=button(r,'All expansions',156,function()end);r.filter:SetPoint('TOPRIGHT')
    end
    r:ClearAllPoints();r:SetPoint('TOPLEFT',0,-y);r:SetSize(F.width,height);r:Show()
    r:SetScript('OnEnter',nil);r:SetScript('OnLeave',nil)
    r:SetScript('OnMouseUp',nil)
    r.toggle:Hide();r.filter:Hide();r.name:Show();r.number:Show();r.detail:Hide()
    r.name:SetWidth(F.width-90);r.detail:SetWidth(F.width-10)
    r:SetBackdropColor(F.used%2==0 and .055 or .075,.045,.075,1);r:SetBackdropBorderColor(0,0,0,0)
    return r
end
function F.Render()
    if not F.frame or not F.db or F.rendering then return end
    F.rendering=true
    local width=F.frame:GetWidth();F.width=width-26;F.body:SetWidth(F.width)
    for _,r in ipairs(F.pool)do r:Hide()end;F.used=0
    F.character:SetWidth(width-186);F.character.caption:SetWidth(width-194)
    F.open:ClearAllPoints();F.open:SetPoint('TOPRIGHT',-102,-33)
    F.refresh:ClearAllPoints();F.refresh:SetPoint('TOPRIGHT',-30,-33)
    F.help:ClearAllPoints();F.help:SetPoint('TOPRIGHT',-5,-33)
    F.status:SetWidth(width-10)
    local c=F.db.characters[F.selected or F.current];local snapshot=c and c.att
    F.character.caption:SetText(M.Plain(c and ((c.name or '?')..'-'..(c.realm or '?')) or 'Current character'))
    local app,message=F.ATTStatus()
    local canRefresh=F.selected==F.current and not F.attBusy
    F.refresh:SetEnabled(canRefresh);F.refresh.caption:SetTextColor(canRefresh and 1 or .55,canRefresh and 1 or .55,canRefresh and 1 or .60)
    F.refresh.caption:SetText(F.attBusy and 'Reading...' or 'Refresh')
    local status=F.attMessage or message or (snapshot and (date('%b %d %I:%M %p',snapshot.seenAt)..' | '..M.Display(snapshot.mode))) or 'Open ATT, then Refresh to capture opportunities.'
    if snapshot and(snapshot.schema or 0)<4 then status='Older capture — Refresh to update ATT instance counts.'end
    F.status:SetText(M.Plain(status))
    F.character:SetScript('OnEnter',nil);F.character:SetScript('OnLeave',nil)
    tooltip(F.character,c and (c.name or '?') or 'Character snapshot',{status,'Offline snapshots are retained. Select a recorded character here.'})
    local y=0
    local target=snapshot and F.GetATDART(snapshot)
    local t=row(y,43);t.name:SetText('ATDART % Target');t.number:SetText(target and string.format('%.2f%%',100*target.progress/target.total) or '')
    t.detail:Show();t.detail:SetText(M.Plain(target and M.Display(target.name) or (snapshot and ((snapshot.schema or 0)<4 and'Refresh to update instance counts.'or snapshot.completion and 'No eligible legacy completion data.' or 'Refresh to capture completion totals.') or 'Enable ATT and capture your first snapshot.')))
    tooltip(t,'ATDART % Target',{target and M.Display(target.name) or 'No eligible completion data.',target and (F.ATTExpansionLabel(target,false)..' | '..target.kind..' | '..target.progress..' / '..target.total..' collected') or 'Refresh with ATT ready to record totals.','Lowest completion across legacy dungeons and raids. Random ties stay fixed until a new capture.'});y=y+45
    F.visibleRows={}
    for _,section in ipairs({{'dungeons','Legacy Dungeons'},{'raids','Legacy Raids'},{'zones','Unfinished Quests'}})do
        local key,title=section[1],section[2];local filter=F.db.settings.filters[key]
        local list={};local expansions={}
        for _,r in ipairs(snapshot and snapshot[key] or {})do
            if key=='zones' or((snapshot.schema or 0)>=4 and F.IsLegacyATT(r))then
                local expansion=F.ATTExpansionLabel(r,key=='zones');expansions[expansion]=true
                if not filter or filter==expansion then list[#list+1]=r end
            end
        end
        F.visibleRows[key]=list
        local header=row(y,22);header.name:Hide();header.number:Hide();header.toggle:Show();header.filter:Show()
        header.toggle:SetWidth(F.width-158);header.toggle.caption:SetWidth(F.width-166)
        header.toggle.caption:SetText((F.db.settings.collapsed[key] and '+ ' or '- ')..title..' ('..#list..')')
        header.toggle:SetScript('OnClick',function()F.db.settings.collapsed[key]=not F.db.settings.collapsed[key];F.Render()end)
        header.filter.caption:SetText(M.Plain(filter or 'All expansions'))
        header.filter:SetScript('OnClick',function()
            local options={{id=false,name='All expansions'}};for name in pairs(expansions)do options[#options+1]={id=name,name=name}end
            table.sort(options,function(a,b)if a.id==false or b.id==false then return a.id==false and b.id~=false end;return a.name<b.name end)
            F.Choose(title..' expansion',options,function(id)F.db.settings.filters[key]=id or nil;F.Render()end)
        end);y=y+24
        if not F.db.settings.collapsed[key]then
            for _,entry in ipairs(list)do
                local r=row(y,22);r.name:SetText(M.Plain(M.Display(entry.name)));r.number:SetText(tostring(entry.missing))
                tooltip(r,M.Display(entry.name),{F.ATTExpansionLabel(entry,key=='zones'),entry.missing..(key=='zones' and ' unfinished quests' or ' missing collectibles'),'Counts follow the ATT profile saved at capture.'});y=y+22
                if key=='zones'then
                    r:SetScript('OnMouseUp',function(_,mouse)if mouse=='LeftButton'and F.DebugReady()then F.ShowQuestDebug(entry,c,snapshot)end end)
                    tooltip(r,M.Display(entry.name),{entry.missing..' unfinished quests','Click for the exact counted IDs and a copyable report.','Use /atdart debug on, then Refresh, for excluded entries and filter diagnostics.'})
                end
            end
            if #list==0 then local r=row(y,22);r.name:SetWidth(F.width-10);r.name:SetText(snapshot and 'No matching opportunities in this snapshot.' or 'No snapshot yet.');r.number:SetText('');y=y+22 end
        end
    end
    F.body:SetHeight(y)
    F.frame:SetHeight(math.max(170,math.min(F.db.settings.height or 520,y+88)))
    F.scroll:SetVerticalScroll(math.min(F.scroll:GetVerticalScroll(),math.max(0,y-F.scroll:GetHeight())))
    F.rendering=false
end
function F.Show(skipInitialCapture)
    if not F.db then F.Init()end;F.Current();F.selected=F.current
    F.CreateWindow();F.frame:Show();F.Render()
    local c=F.db.characters[F.current];if not skipInitialCapture and c and not c.att and not F.attBusy then F.RefreshATT()end
end

