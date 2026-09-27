USE StudentPlacementDB;
GO

-- 1. Students Table
CREATE TABLE Students
(
    StudentID INT IDENTITY(1,1) PRIMARY KEY,
    StudentName NVARCHAR(100) NOT NULL
);
GO


-- 2. Academic Details Table
CREATE TABLE AcademicDetails
(
    AcademicID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL,
    Marks10th DECIMAL(5,2) NOT NULL,
    Marks12th DECIMAL(5,2) NOT NULL,
    CGPA DECIMAL(4,2) NOT NULL,

    CONSTRAINT FK_Academic_Student
        FOREIGN KEY (StudentID)
        REFERENCES Students(StudentID),

    CONSTRAINT CK_Academic_Marks10th
        CHECK (Marks10th BETWEEN 0 AND 100),

    CONSTRAINT CK_Academic_Marks12th
        CHECK (Marks12th BETWEEN 0 AND 100),

    CONSTRAINT CK_Academic_CGPA
        CHECK (CGPA BETWEEN 0 AND 10)
);
GO


-- 3. Skills Table
CREATE TABLE Skills
(
    SkillID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL,
    TechnicalSkills NVARCHAR(500),
    Certifications NVARCHAR(500),

    CONSTRAINT FK_Skills_Student
        FOREIGN KEY (StudentID)
        REFERENCES Students(StudentID)
);
GO


-- 4. Projects Table
CREATE TABLE Projects
(
    ProjectID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL,
    ProjectCount INT NOT NULL,

    CONSTRAINT FK_Projects_Student
        FOREIGN KEY (StudentID)
        REFERENCES Students(StudentID),

    CONSTRAINT CK_ProjectCount
        CHECK (ProjectCount >= 0)
);
GO


-- 5. Internships Table
CREATE TABLE Internships
(
    InternshipID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL,
    InternshipStatus NVARCHAR(20) NOT NULL,

    CONSTRAINT FK_Internship_Student
        FOREIGN KEY (StudentID)
        REFERENCES Students(StudentID),

    CONSTRAINT CK_InternshipStatus
        CHECK (InternshipStatus IN ('Yes', 'No'))
);
GO


-- 6. Scores Table
CREATE TABLE Scores
(
    ScoreID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL,
    CodingScore DECIMAL(5,2) NOT NULL,
    AptitudeScore DECIMAL(5,2) NOT NULL,
    CommunicationScore DECIMAL(5,2) NOT NULL,

    CONSTRAINT FK_Scores_Student
        FOREIGN KEY (StudentID)
        REFERENCES Students(StudentID),

    CONSTRAINT CK_CodingScore
        CHECK (CodingScore BETWEEN 0 AND 100),

    CONSTRAINT CK_AptitudeScore
        CHECK (AptitudeScore BETWEEN 0 AND 100),

    CONSTRAINT CK_CommunicationScore
        CHECK (CommunicationScore BETWEEN 0 AND 100)
);
GO


-- 7. Placement Details Table
CREATE TABLE PlacementDetails
(
    PlacementID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL,
    PlacementStatus NVARCHAR(20) NOT NULL,

    CONSTRAINT FK_Placement_Student
        FOREIGN KEY (StudentID)
        REFERENCES Students(StudentID),

    CONSTRAINT CK_PlacementStatus
        CHECK (PlacementStatus IN ('Placed', 'Not Placed'))
);
GO