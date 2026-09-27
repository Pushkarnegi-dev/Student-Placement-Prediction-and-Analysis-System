import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import textwrap
import html


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student Placement Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HTML HELPER
# ============================================================

def html_block(content):
    st.html(textwrap.dedent(content).strip())


# ============================================================
# DATA LOAD
# ============================================================

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "Data"
    / "cleaned_student_data.csv"
)


@st.cache_data
def load_data():

    data = pd.read_csv(DATA_PATH)

    numeric_columns = [
        "StudentID",
        "Marks10th",
        "Marks12th",
        "CGPA",
        "ProjectCount",
        "CodingScore",
        "AptitudeScore",
        "CommunicationScore"
    ]

    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(
                data[col],
                errors="coerce"
            )

    text_columns = [
        "StudentName",
        "Course",
        "Specialization",
        "TechnicalSkills",
        "Certifications",
        "InternshipStatus",
        "PlacementStatus"
    ]

    for col in text_columns:
        if col in data.columns:
            data[col] = (
                data[col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return data


df = load_data()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "StudentID",
    "StudentName",
    "Course",
    "Specialization",
    "CGPA",
    "CodingScore",
    "AptitudeScore",
    "CommunicationScore",
    "PlacementStatus"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "Required columns missing from cleaned_student_data.csv: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   MAIN
============================================================ */

.stApp {
    background: #061321;
    color: white;
}

.block-container {
    max-width: 100%;
    padding: 12px 18px 25px 18px;
}

#MainMenu {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    display: none !important;
}

div[data-testid="stToolbar"] {
    display: none !important;
}


div[data-testid="stAppDeployButton"] {
    display: none !important;
}

footer {
    visibility: hidden;
}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {
    background: #061426 !important;
    border-right: 1px solid #1b3959;
    min-width: 270px !important;
    max-width: 270px !important;
}

section[data-testid="stSidebar"] > div {
    padding: 16px 10px;
}

.portal-title {
    color: #ffffff;
    font-size: 23px;
    font-weight: 800;
}

.portal-subtitle {
    color: #7f96b0;
    font-size: 13px;
    margin-top: 4px;
}

.sidebar-line {
    height: 1px;
    background: #1c3651;
    margin: 14px 0;
}

.sidebar-active {
    background: linear-gradient(
        90deg,
        #1169e8,
        #1761d4
    );
    border-radius: 8px;
    padding: 12px 13px;
    color: white;
    font-size: 12px;
    font-weight: 700;
}

.sidebar-item {
    color: #a9b9ce;
    padding: 11px 13px;
    font-size: 14px;
    border-radius: 7px;
    margin-top: 2px;
}

.sidebar-lock {
    float: right;
    color: #f2b83f;
}


/* ============================================================
   MOUNTAINS
============================================================ */

.mountain-area {
    position: relative;
    height: 155px;
    margin-top: 65px;
    overflow: hidden;
}

.mountain {
    position: absolute;
    bottom: -8px;
    width: 0;
    height: 0;
    border-left: 75px solid transparent;
    border-right: 75px solid transparent;
}

.m1 {
    left: -45px;
    border-bottom: 110px solid #0c2a47;
}

.m2 {
    left: 25px;
    border-left-width: 88px;
    border-right-width: 88px;
    border-bottom: 145px solid #09243f;
}

.m3 {
    left: 135px;
    border-bottom: 125px solid #0d2d4c;
}

.m4 {
    left: 215px;
    border-bottom: 140px solid #09243f;
}

.mountain-ground {
    position: absolute;
    left: -20px;
    bottom: -20px;
    width: 330px;
    height: 80px;
    background: #071b2e;
    clip-path: polygon(
        0 100%,
        12% 63%,
        25% 78%,
        40% 38%,
        52% 70%,
        68% 45%,
        82% 74%,
        100% 50%,
        100% 100%
    );
}

.sidebar-quote {
    text-align: center;
    color: #70859e;
    font-size: 9px;
    font-style: italic;
    line-height: 1.5;
}


/* ============================================================
   HEADER
============================================================ */

.header-box {
    background: #071a2e;
    border: 1px solid #1b3959;
    border-radius: 10px;
    padding: 16px 18px;
    min-height: 105px;
}

.header-title {
    color: white;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.1;
}

.header-blue {
    color: #2586ff;
}

.header-subtitle {
    color: #91a5bd;
    font-size: 12px;
    margin-top: 6px;
}

.review-badge {
    display: inline-block;
    margin-top: 9px;
    padding: 7px 12px;
    border-radius: 18px;
    background: #102b4b;
    border: 1px solid #28578d;
    color: #dbe8f8;
    font-size: 9px;
}

.updated-box {
    background: #0b203a;
    border: 1px solid #24496f;
    border-radius: 9px;
    padding: 12px;
    text-align: center;
    margin-top: 3px;
}

.updated-label {
    color: #7188a4;
    font-size: 13px;
}

.updated-date {
    color: white;
    font-size: 12px;
    font-weight: 700;
    margin-top: 3px;
}


/* ============================================================
   METRIC CARDS
============================================================ */

.metric-card {
    background: #0b1d33;
    border: 1px solid #1b3b5d;
    border-radius: 10px;
    min-height: 95px;
    padding: 13px;
}

.metric-icon {
    float: left;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-right: 10px;
}

.icon-blue {
    background: #0a438a;
}

.icon-green {
    background: #075f43;
}

.icon-red {
    background: #681d38;
}

.icon-purple {
    background: #43206e;
}

.metric-label {
    color: #a7b7ca;
    font-size: 14px;
}

.metric-value {
    color: white;
    font-size: 32px;
    font-weight: 800;
    line-height: 1.2;
}

.metric-sub {
    color: #71869f;
    font-size: 12px;
}

.green {
    color: #2cdd83;
}

.red {
    color: #ff4b69;
}

.purple {
    color: #b16cff;
}


/* ============================================================
   FILTER BOX
============================================================ */

.filter-box {
    background: #091b30;
    border: 1px solid #1b3959;
    border-radius: 10px;
    padding: 9px 13px;
}

.filter-title {
    color: white;
    font-size: 14px;
    font-weight: 700;
}


/* ============================================================
   STREAMLIT INPUTS
============================================================ */

div[data-baseweb="select"] > div {
    background: #0b1c32 !important;
    border-color: #294766 !important;
}

div[data-baseweb="select"] span {
    color: #e8eef7 !important;
}

label {
    color: #91a5be !important;
    font-size: 9px !important;
}

.stFormSubmitButton > button {
    background: #126be9 !important;
    border: 1px solid #3983ef !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    min-height: 38px !important;
}

div[data-testid="stTextInput"] input {
    background: #101d30 !important;
    color: white !important;
    border: 1px solid #203d5d !important;
    border-radius: 7px !important;
    font-size: 14px !important;
}


/* ============================================================
   CHART TITLES
============================================================ */

.chart-title-box {
    background: #091a2e;
    border: 1px solid #1b3959;
    border-radius: 10px 10px 0 0;
    padding: 9px 12px 5px 12px;
    color: white;
    font-size: 12px;
    font-weight: 700;
}


/* ============================================================
   TABLE
============================================================ */

.table-title-box {
    background: #091a2e;
    border: 1px solid #1b3959;
    border-radius: 10px 10px 0 0;
    padding: 10px 12px;
    color: white;
    font-size: 14px;
    font-weight: 700;
}

.student-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

.student-table th {
    background: #112744;
    color: #b7c6d8;
    padding: 9px 7px;
    text-align: left;
    border-bottom: 1px solid #203b58;
    white-space: nowrap;
}

.student-table td {
    background: #081526;
    color: #dbe4ee;
    padding: 8px 7px;
    border-bottom: 1px solid #172b42;
    white-space: nowrap;
}

.student-table tr:nth-child(even) td {
    background: #0a192b;
}

.status-placed {
    background: #087942;
    color: white;
    border-radius: 12px;
    padding: 4px 9px;
    font-weight: 700;
}

.status-not {
    background: #c72d4c;
    color: white;
    border-radius: 12px;
    padding: 4px 9px;
    font-weight: 700;
}

.page-info {
    color: #7388a3;
    text-align: center;
    font-size: 9px;
    padding: 8px;
}

.stButton > button {
    background: #0b2038;
    color: white;
    border: 1px solid #294766;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html_block("""
        <div class="portal-title">🎓 Placement Portal</div>
        <div class="portal-subtitle">
            Student Placement Analysis System
        </div>
    """)

    html_block("""
        <div class="sidebar-line"></div>

        <div class="sidebar-active">
            🏠 &nbsp; Dashboard
        </div>
    """)

    sidebar_items = [
        "👥 &nbsp; Students",
        "📋 &nbsp; Academic Details",
        "⚙️ &nbsp; Skills",
        "📁 &nbsp; Projects",
        "💼 &nbsp; Internships",
        "📝 &nbsp; Assessments",
        "📊 &nbsp; Analytics",
        "📄 &nbsp; Reports"
    ]

    for item in sidebar_items:

        html_block(f"""
            <div class="sidebar-item">
                {item}
                <span class="sidebar-lock">🔒</span>
            </div>
        """)

    html_block("""
        <div class="mountain-area">
            <div class="mountain m1"></div>
            <div class="mountain m2"></div>
            <div class="mountain m3"></div>
            <div class="mountain m4"></div>
            <div class="mountain-ground"></div>
        </div>

        <div class="sidebar-quote">
            "Better Insights Today,<br>
            Brighter Careers Tomorrow"
        </div>
    """)


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([5.5, 1])

with header_left:

    html_block("""
        <div class="header-box">

            <div class="header-title">
                Student
                <span class="header-blue">Placement</span>
                Dashboard
            </div>

            <div class="header-subtitle">
                Analyse • Predict • Empower Students
            </div>

            <div class="review-badge">
                ● &nbsp; Currently showing only Placement Status
                module (Review 1)
            </div>

        </div>
    """)

with header_right:

    html_block("""
        <div class="updated-box">
            <div class="updated-label">
                LAST UPDATED
            </div>

            <div class="updated-date">
                28 Sep 2026
            </div>
        </div>
    """)


# ============================================================
# FILTER STATE
# ============================================================

if "selected_course" not in st.session_state:
    st.session_state.selected_course = "All Courses"

if "selected_specialization" not in st.session_state:
    st.session_state.selected_specialization = "All Specializations"

if "selected_placement" not in st.session_state:
    st.session_state.selected_placement = "All Students"

if "selected_cgpa" not in st.session_state:

    st.session_state.selected_cgpa = (
        float(df["CGPA"].min()),
        float(df["CGPA"].max())
    )

if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = 1


# ============================================================
# APPLY FILTERS TO DATA
# ============================================================

filtered_df = df.copy()


if st.session_state.selected_course != "All Courses":

    filtered_df = filtered_df[
        filtered_df["Course"]
        .eq(st.session_state.selected_course)
    ].copy()


if (
    st.session_state.selected_specialization
    != "All Specializations"
):

    filtered_df = filtered_df[
        filtered_df["Specialization"]
        .eq(
            st.session_state.selected_specialization
        )
    ].copy()


if st.session_state.selected_placement != "All Students":

    filtered_df = filtered_df[
        filtered_df["PlacementStatus"]
        .eq(
            st.session_state.selected_placement
        )
    ].copy()


filtered_df = filtered_df[
    (
        filtered_df["CGPA"]
        >= st.session_state.selected_cgpa[0]
    )
    &
    (
        filtered_df["CGPA"]
        <= st.session_state.selected_cgpa[1]
    )
].copy()


# ============================================================
# PLACEMENT FLAG
# ============================================================

filtered_df["PlacedFlag"] = (
    filtered_df["PlacementStatus"]
    .eq("Placed")
    .astype(int)
)


# ============================================================
# METRICS
# ============================================================

total_students = len(filtered_df)

placed_students = int(
    filtered_df["PlacedFlag"].sum()
)

not_placed_students = (
    total_students - placed_students
)

placement_rate = (
    placed_students / total_students * 100
    if total_students > 0
    else 0
)

not_placed_rate = (
    not_placed_students / total_students * 100
    if total_students > 0
    else 0
)

average_cgpa = (
    float(filtered_df["CGPA"].mean())
    if total_students > 0
    else 0
)


# ============================================================
# METRIC CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    html_block(f"""
        <div class="metric-card">

            <div class="metric-icon icon-blue">
                👥
            </div>

            <div class="metric-label">
                Total Students
            </div>

            <div class="metric-value">
                {total_students}
            </div>

            <div class="metric-sub">
                From database
            </div>

        </div>
    """)

with c2:

    html_block(f"""
        <div class="metric-card">

            <div class="metric-icon icon-green">
                💼
            </div>

            <div class="metric-label">
                Placed Students
            </div>

            <div class="metric-value green">
                {placed_students}
            </div>

            <div class="metric-sub green">
                {placement_rate:.1f}% placement rate
            </div>

        </div>
    """)

with c3:

    html_block(f"""
        <div class="metric-card">

            <div class="metric-icon icon-red">
                👤
            </div>

            <div class="metric-label">
                Not Placed Students
            </div>

            <div class="metric-value red">
                {not_placed_students}
            </div>

            <div class="metric-sub red">
                {not_placed_rate:.1f}%
            </div>

        </div>
    """)

with c4:

    html_block(f"""
        <div class="metric-card">

            <div class="metric-icon icon-purple">
                📊
            </div>

            <div class="metric-label">
                Average CGPA
            </div>

            <div class="metric-value purple">
                {average_cgpa:.2f}
            </div>

            <div class="metric-sub">
                Across selected students
            </div>

        </div>
    """)


# ============================================================
# FILTER BOX
# ============================================================

html_block("""
    <div class="filter-box">
        <div class="filter-title">
            🔽 &nbsp; Filters
        </div>
    </div>
""")


# ============================================================
# FILTER CONTROLS
# ============================================================

with st.form("dashboard_filters"):

    f1, f2, f3, f4, f5 = st.columns(
        [1.05, 1.25, 1.05, 1.35, 0.8]
    )

    with f1:

        course_options = (
            ["All Courses"]
            +
            sorted(
                df["Course"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        course_choice = st.selectbox(
            "Course / Degree",
            course_options,
            index=course_options.index(
                st.session_state.selected_course
            )
        )

    with f2:

        specialization_options = (
            ["All Specializations"]
            +
            sorted(
                df["Specialization"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        specialization_choice = st.selectbox(
            "Branch / Specialization",
            specialization_options,
            index=specialization_options.index(
                st.session_state.selected_specialization
            )
        )

    with f3:

        placement_options = [
            "All Students",
            "Placed",
            "Not Placed"
        ]

        placement_choice = st.selectbox(
            "Placement Status",
            placement_options,
            index=placement_options.index(
                st.session_state.selected_placement
            )
        )

    with f4:

        min_cgpa = float(df["CGPA"].min())
        max_cgpa = float(df["CGPA"].max())

        cgpa_choice = st.slider(
            "CGPA Range",
            min_value=min_cgpa,
            max_value=max_cgpa,
            value=st.session_state.selected_cgpa,
            step=0.1
        )

    with f5:

        st.write("")

        apply_filters = st.form_submit_button(
            "🔎 Apply Filters",
            use_container_width=True
        )


# ============================================================
# SAVE FILTERS
# ============================================================

if apply_filters:

    st.session_state.selected_course = course_choice

    st.session_state.selected_specialization = (
        specialization_choice
    )

    st.session_state.selected_placement = (
        placement_choice
    )

    st.session_state.selected_cgpa = cgpa_choice

    st.session_state.dashboard_page = 1

    st.rerun()


# ============================================================
# CHART 1 - PLACEMENT STATUS
# ============================================================

chart1, chart2, chart3 = st.columns(3)


with chart1:

    html_block("""
        <div class="chart-title-box">
            🔵 &nbsp; Placement Status Distribution
        </div>
    """)

    fig1 = go.Figure(
        go.Pie(
            labels=[
                "Placed",
                "Not Placed"
            ],
            values=[
                placed_students,
                not_placed_students
            ],
            hole=0.58,
            marker=dict(
                colors=[
                    "#1685ff",
                    "#ff3f60"
                ],
                line=dict(
                    color="#091a2e",
                    width=3
                )
            ),
            textinfo="percent",
            textfont=dict(
                color="white",
                size=12
            )
        )
    )

    fig1.add_annotation(
        x=0.5,
        y=0.5,
        text=(
            f"<b>{total_students}</b>"
            "<br>"
            "<span style='font-size:10px'>Students</span>"
        ),
        showarrow=False,
        font=dict(
            color="white",
            size=17
        )
    )

    fig1.update_layout(
        paper_bgcolor="#091a2e",
        plot_bgcolor="#091a2e",
        height=270,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),
        font=dict(color="white"),
        legend=dict(
            font=dict(color="white")
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# CHART 2 - COURSE
# ============================================================

with chart2:

    html_block("""
        <div class="chart-title-box">
            📊 &nbsp; Course-wise Placement Rate
        </div>
    """)

    course_total = (
        filtered_df
        .groupby("Course")
        .size()
        .reset_index(name="Total")
    )

    course_placed = (
        filtered_df[
            filtered_df["PlacedFlag"] == 1
        ]
        .groupby("Course")
        .size()
        .reset_index(name="Placed")
    )

    course_data = course_total.merge(
        course_placed,
        on="Course",
        how="left"
    )

    course_data["Total"] = pd.to_numeric(
        course_data["Total"],
        errors="coerce"
    ).fillna(0)

    course_data["Placed"] = pd.to_numeric(
        course_data["Placed"],
        errors="coerce"
    ).fillna(0)

    course_data["Rate"] = (
        course_data["Placed"].astype(float)
        /
        course_data["Total"].astype(float)
        * 100
    )

    course_colors = [
        "#8d5cf6",
        "#287ff0",
        "#ed4b91",
        "#f3a33f",
        "#3db9dd"
    ]

    fig2 = go.Figure(
        go.Bar(
            x=course_data["Course"].tolist(),
            y=course_data["Rate"].tolist(),
            text=[
                f"{float(x):.0f}%"
                for x in course_data["Rate"]
            ],
            textposition="outside",
            marker_color=[
                course_colors[
                    i % len(course_colors)
                ]
                for i in range(len(course_data))
            ]
        )
    )

    fig2.update_layout(
        paper_bgcolor="#091a2e",
        plot_bgcolor="#091a2e",
        height=270,
        margin=dict(
            l=45,
            r=10,
            t=10,
            b=40
        ),
        font=dict(color="white")
    )

    fig2.update_yaxes(
        range=[0, 100],
        title="Placement Rate (%)",
        gridcolor="#19324d"
    )

    fig2.update_xaxes(
        gridcolor="#19324d"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# CHART 3 - SPECIALIZATION
# ============================================================

with chart3:

    html_block("""
        <div class="chart-title-box">
            📚 &nbsp; Branch/Specialization-wise Placement Rate
        </div>
    """)

    specialization_total = (
        filtered_df
        .groupby("Specialization")
        .size()
        .reset_index(name="Total")
    )

    specialization_placed = (
        filtered_df[
            filtered_df["PlacedFlag"] == 1
        ]
        .groupby("Specialization")
        .size()
        .reset_index(name="Placed")
    )

    specialization_data = (
        specialization_total.merge(
            specialization_placed,
            on="Specialization",
            how="left"
        )
    )

    specialization_data["Total"] = pd.to_numeric(
        specialization_data["Total"],
        errors="coerce"
    ).fillna(0)

    specialization_data["Placed"] = pd.to_numeric(
        specialization_data["Placed"],
        errors="coerce"
    ).fillna(0)

    specialization_data["Rate"] = (
        specialization_data["Placed"].astype(float)
        /
        specialization_data["Total"].astype(float)
        * 100
    )

    specialization_colors = [
        "#43d28c",
        "#32c4df",
        "#3b82f6",
        "#9856e8",
        "#e94e9b",
        "#f29e38"
    ]

    fig3 = go.Figure(
        go.Bar(
            x=specialization_data[
                "Specialization"
            ].tolist(),
            y=specialization_data[
                "Rate"
            ].tolist(),
            text=[
                f"{float(x):.0f}%"
                for x in specialization_data["Rate"]
            ],
            textposition="outside",
            marker_color=[
                specialization_colors[
                    i % len(specialization_colors)
                ]
                for i in range(
                    len(specialization_data)
                )
            ]
        )
    )

    fig3.update_layout(
        paper_bgcolor="#091a2e",
        plot_bgcolor="#091a2e",
        height=270,
        margin=dict(
            l=45,
            r=10,
            t=10,
            b=60
        ),
        font=dict(color="white")
    )

    fig3.update_yaxes(
        range=[0, 100],
        title="Placement Rate (%)",
        gridcolor="#19324d"
    )

    fig3.update_xaxes(
        tickangle=-25,
        gridcolor="#19324d"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# STUDENT PLACEMENT DETAILS
# ============================================================

html_block("""
    <div class="table-title-box">
        👥 &nbsp; Student Placement Details
    </div>
""")


# ============================================================
# SEARCH
# ============================================================

search_text = st.text_input(
    "Search",
    placeholder="🔍  Search by name, ID or course...",
    label_visibility="collapsed"
)


table_df = filtered_df.copy()


if search_text:

    search_value = (
        search_text
        .strip()
        .lower()
    )

    mask = (
        table_df["StudentID"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_value,
            na=False
        )
        |
        table_df["StudentName"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_value,
            na=False
        )
        |
        table_df["Course"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_value,
            na=False
        )
        |
        table_df["Specialization"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_value,
            na=False
        )
    )

    table_df = table_df[mask].copy()


# ============================================================
# PAGINATION
# ============================================================

rows_per_page = 8

total_pages = max(
    1,
    (
        len(table_df)
        + rows_per_page
        - 1
    )
    // rows_per_page
)

if st.session_state.dashboard_page > total_pages:
    st.session_state.dashboard_page = total_pages

current_page = st.session_state.dashboard_page

start_index = (
    current_page - 1
) * rows_per_page

end_index = (
    start_index
    + rows_per_page
)

page_data = table_df.iloc[
    start_index:end_index
].copy()


# ============================================================
# TABLE
# ============================================================

table_html = """
<table class="student-table">

<thead>
<tr>
    <th>#</th>
    <th>Student ID</th>
    <th>Student Name</th>
    <th>Course</th>
    <th>Branch / Specialization</th>
    <th>CGPA</th>
    <th>Coding Score</th>
    <th>Aptitude Score</th>
    <th>Communication Score</th>
    <th>Placement Status</th>
</tr>
</thead>

<tbody>
"""


for number, (_, row) in enumerate(
    page_data.iterrows(),
    start=start_index + 1
):

    student_id = html.escape(
        str(row["StudentID"])
    )

    student_name = html.escape(
        str(row["StudentName"])
    )

    course = html.escape(
        str(row["Course"])
    )

    specialization = html.escape(
        str(row["Specialization"])
    )

    cgpa = (
        f"{float(row['CGPA']):.1f}"
    )

    coding = (
        f"{float(row['CodingScore']):.0f}"
    )

    aptitude = (
        f"{float(row['AptitudeScore']):.0f}"
    )

    communication = (
        f"{float(row['CommunicationScore']):.0f}"
    )

    status = str(
        row["PlacementStatus"]
    )

    if status == "Placed":

        status_html = (
            '<span class="status-placed">'
            '✓ Placed'
            '</span>'
        )

    else:

        status_html = (
            '<span class="status-not">'
            '✕ Not Placed'
            '</span>'
        )

    table_html += f"""
<tr>
    <td>{number}</td>
    <td>{student_id}</td>
    <td>{student_name}</td>
    <td>{course}</td>
    <td>{specialization}</td>
    <td>{cgpa}</td>
    <td>{coding}</td>
    <td>{aptitude}</td>
    <td>{communication}</td>
    <td>{status_html}</td>
</tr>
"""


table_html += """
</tbody>
</table>
"""


st.html(table_html)


# ============================================================
# PAGINATION CONTROLS
# ============================================================

prev_col, info_col, next_col = st.columns(
    [1, 6, 1]
)


with prev_col:

    previous_clicked = st.button(
        "‹",
        disabled=(
            current_page == 1
        ),
        use_container_width=True
    )

    if previous_clicked:

        st.session_state.dashboard_page -= 1

        st.rerun()


with info_col:

    first_record = (
        start_index + 1
        if len(table_df) > 0
        else 0
    )

    last_record = min(
        end_index,
        len(table_df)
    )

    html_block(f"""
        <div class="page-info">
            Showing {first_record}-{last_record}
            of {len(table_df)} students
            &nbsp; • &nbsp;
            Page {current_page} of {total_pages}
        </div>
    """)


with next_col:

    next_clicked = st.button(
        "›",
        disabled=(
            current_page == total_pages
        ),
        use_container_width=True
    )

    if next_clicked:

        st.session_state.dashboard_page += 1

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

html_block("""
    <div style="
        text-align:center;
        color:#536b88;
        font-size:9px;
        padding:10px;
    ">
        Student Placement Prediction and Analysis System
        • Review 1
    </div>
""")