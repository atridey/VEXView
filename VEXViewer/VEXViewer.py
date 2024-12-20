import reflex as rx
from . import RECData
from rxconfig import config
from datetime import datetime
from typing import List
import asyncio

class State(rx.State):
    teamNum = ""
    teamID = 0
    teamName = ""
    robotName = ""
    school = ""
    location = ""
    competitions: List[dict] = []

    eventID = 0
    eventTimestamp = ""
    matches: List[dict] = []

    currentTime = ""

    @rx.event(background=True)
    async def updateTime(self):
        timeZone = datetime.fromisoformat(self.eventTimestamp).tzinfo
        while True:
            async with self:
                self.currentTime = datetime.now(timeZone).strftime("%H:%M:%S")
            await asyncio.sleep(0.1)

    def updateTeamNum(self, num):
        self.teamNum = num

    @rx.event
    def updateEvent(self, id: int):
        self.eventID = id
        
        competition: dict = {}
        for aCompetition in self.competitions:
            if aCompetition['id'] == self.eventID:
                competition = aCompetition
        self.eventTimestamp = competition['startTimestamp']
        self.updateMatchList()
        
    def setTeamInfo(self):
        teamInfo = RECData.teamInfo(self.teamNum)
        self.teamID = teamInfo['id']
        self.teamName = teamInfo['teamName']
        self.robotName = teamInfo['robotName']
        self.school = teamInfo['school']
        self.location = teamInfo['location']

        self.competitions = RECData.recentEvents(self.teamID)
        
    def updateMatchList(self):
        competition: dict = {}
        for aCompetition in self.competitions:
            if aCompetition['id'] == self.eventID:
                competition = aCompetition
        self.matches = RECData.getMatches(competition, self.teamNum)


#A bunch of leftover template functions - kept for future functionality expansion
def create_nav_link(text):
    """Create a navigation link with hover effect."""
    return rx.el.a(text, href="#", _hover={"color": "#D1D5DB"})

def create_nav_item(text):
    """Create a navigation item containing a link."""
    return rx.el.li(create_nav_link(text=text))


def create_section_heading(text):
    """Create a section heading with specific styling."""
    return rx.heading(
        text,
        font_weight="600",
        margin_bottom="1rem",
        font_size="1.25rem",
        line_height="1.75rem",
        as_="h2",
    )

def create_bold_text(text):
    return rx.text(text, font_weight="700")
    
def create_normal_text(text):
    return rx.text(text)


def create_labeled_info(label, value):
    return rx.box(
        create_bold_text(text=label),
        create_normal_text(text=value),
    )


def create_subsection_heading(text):
    return rx.heading(text, font_weight="700", as_="h3", size="4")


def create_gray_text(text):
    return rx.text(text, color="#9CA3AF")


def create_view_schedule_button(value: rx.Var[int]) -> rx.Component:
    return rx.el.button(
        "View Schedule",
        background_color="#2563EB",
        transition_duration="300ms",
        _hover={"background-color": "#1D4ED8"},
        margin_top="1rem",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.375rem",
        color="#ffffff",
        transition_property=
        "background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=State.updateEvent(value),
    )

def create_competition_card(competition: rx.Var[dict]) -> rx.Component:
    return rx.box(
        create_subsection_heading(text=competition['name']),
        create_gray_text(text=competition['date']),
        create_gray_text(text=competition['location']),
        create_view_schedule_button(competition['id']), #For testing purposes: Chittenango is 58047
        background_color="#1F2937",
        padding="1rem",
        border_radius="0.375rem",
    )

def create_table_header_cell(text):
    return rx.table.column_header_cell(text,
                                       padding="0.5rem",
                                       text_align="left")

def create_table_cell(content):
    return rx.table.cell(content, padding="0.5rem")

def create_match_row(match):
    return rx.table.row(
        create_table_cell(content=match['name']),
        create_table_cell(content=match['scheduled']),
        create_table_cell(content=match['field']),
        create_table_cell(content=match['redAlliance']),
        create_table_cell(content=match['blueAlliance']),
        on_mount=State.updateTime, #This requires reload in current form, may try a different event handler. 
    )


def create_header():
    return rx.flex(
        rx.heading(
            "VEXViewer",
            font_weight="700",
            font_size="1.5rem",
            line_height="2rem",
            as_="h1",
        ),
        rx.list(
            create_nav_item(text="Home"),
            create_nav_item(text="About"),
            create_nav_item(text="Contact"),
            display="flex",
            column_gap="1rem",
        ),
        width="100%",
        style=rx.breakpoints({
            "640px": {
                "max-width": "640px"
            },
            "768px": {
                "max-width": "768px"
            },
            "1024px": {
                "max-width": "1024px"
            },
            "1280px": {
                "max-width": "1280px"
            },
            "1536px": {
                "max-width": "1536px"
            },
        }),
        display="flex",
        align_items="center",
        justify_content="space-between",
        margin_left="auto",
        margin_right="auto",
    )


def create_search_button():
    return rx.el.button(
        "Search",
        background_color="#2563EB",
        transition_duration="300ms",
        _hover={"background-color": "#1D4ED8"},
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_top_right_radius="0.375rem",
        border_bottom_right_radius="0.375rem",
        color="#ffffff",
        transition_property=
        "background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=State.setTeamInfo,
    )

def create_search_bar():
    return rx.flex(
        rx.el.input(
            placeholder="Team Number (incl. letter)", #Need user feedback to determine most clear message
            type="text",
            background_color="#374151",
            _focus={
                "outline-style": "none",
                "box-shadow":
                "var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)",
                "--ring-color": "#3B82F6",
            },
            padding="0.5rem",
            border_top_left_radius="0.375rem",
            border_bottom_left_radius="0.375rem",
            color="#ffffff",
            on_change=State.updateTeamNum,
        ),
        create_search_button(),
        display="flex",
    )


def create_team_info_section():
    return rx.box(
        create_section_heading(text="Team Information"),
        rx.box(
            create_labeled_info(label="Team Name:", value=State.teamName),
            create_labeled_info(label="Robot Name:", value=State.robotName),
            create_labeled_info(label="School:", value=State.school),
            create_labeled_info(label="Location:", value=State.location),
            gap="1rem",
            display="grid",
            grid_template_columns="repeat(2, minmax(0, 1fr))",
        ),
        background_color="#1F2937",
        margin_bottom="2rem",
        padding="1.5rem",
        border_radius="0.5rem",
    )


def create_match_schedule_table():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                create_table_header_cell(text="Match"),
                create_table_header_cell(text="Scheduled"),
                create_table_header_cell(text="Field"),
                create_table_header_cell(text="Red Alliance"),
                create_table_header_cell(text="Blue Alliance"),
                background_color="#374151",
            )),
        rx.table.body(
            rx.foreach(State.matches, create_match_row),
        ),
        background_color="#1F2937",
        border_radius="0.375rem",
        width="100%",
    )


def create_main_content():
    return rx.box(
        rx.box(
            create_section_heading(text="Enter Your Team Number"),
            create_search_bar(),
            margin_bottom="2rem",
        ),
        create_team_info_section(),
        rx.box(
            create_section_heading(text=str(datetime.now().year) + '-' + str(datetime.now().year+1)[2:] + ' Competitions'),
            rx.box(
                rx.foreach(State.competitions, create_competition_card),

                gap="1rem",
                display="grid",
                grid_template_columns=rx.breakpoints({
                    "0px":
                    "repeat(1, minmax(0, 1fr))",
                    "768px":
                    "repeat(2, minmax(0, 1fr))",
                    "1024px":
                    "repeat(3, minmax(0, 1fr))",
                }),
            ),
            margin_bottom="2rem",
        ),
        rx.box(
            #Header and clock flexbox
            rx.box(
                create_section_heading(text="Match Schedule"),
                rx.text(
                    State.currentTime,
                    font_size="1.25rem",
                    color="gray.500",
                ),
                display="flex",
                justify_content="space-between",  #Distribute
                align_items="center",
                margin_bottom="0.5rem",
            ),
            rx.box(
                create_match_schedule_table(),
                overflow_x="auto",
            ),
        ),
        width="100%",
        style=rx.breakpoints({
            "640px": {
                "max-width": "640px"
            },
            "768px": {
                "max-width": "768px"
            },
            "1024px": {
                "max-width": "1024px"
            },
            "1280px": {
                "max-width": "1280px"
            },
            "1536px": {
                "max-width": "1536px"
            },
        }),
        flex_grow="1",
        margin_left="auto",
        margin_right="auto",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="2rem",
        padding_bottom="2rem",
    )


def create_page_layout():
    return rx.box(
        rx.box(
            create_header(),
            background_color="#1F2937",
            padding="1rem",
        ),
        create_main_content(),
        rx.box(
            rx.text(
                "Made with ❤️ by 5501B",
                color="#9CA3AF",
                font_size="0.875rem",
                line_height="1.25rem",
            ),
            rx.text(
                "© 2024 Atri Dey", #At least I hope that's how copyright works
                color="#9CA3AF",
                font_size="0.875rem",
                line_height="1.25rem",
            ),
            background_color="#111827",
            padding="1rem",
            text_align="center",
        ),
        display="flex",
        flex_direction="column",
        min_height="100vh",
    )

def index():
    #Final render
    return rx.fragment(
        rx.script(src="https://cdn.tailwindcss.com"),
        rx.el.style("""
        @font-face {
            font-family: 'LucideIcons';
            src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
        }
    """),
        create_page_layout(),
    )


app = rx.App()
app.add_page(index)
