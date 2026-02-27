#flowdiagram 
``` @startuml
title Autonomous Social Media Agent

start

:Load Configuration;
note right
Page ID
Access Token
Group IDs
Posts per day
Tone / Niche
end note

:Scheduler Trigger (5x Daily);

:Fetch Trending Topics;

:Filter by Niche;

:Rank & Score Topics;

if (High Score Topic?) then (Yes)
    :Generate Post Caption & Hashtags;
    :Generate Image (AI);
    :Generate Video (AI);
    
    :Upload Media to Facebook;
    :Create Page Post;
    
    if (Share to Groups Enabled?) then (Yes)
        :Share Post to Groups;
    endif
    
    :Fetch Engagement Metrics;
    :Store Analytics in Database;
    
    :Optimize Future Content;
else (No)
    :Wait for Next Trend Cycle;
endif

stop
@enduml```