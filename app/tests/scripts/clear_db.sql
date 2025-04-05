IF OBJECT_ID (N'dbo.booking_dates', N'U') IS NOT NULL
    TRUNCATE TABLE dbo.booking_dates;

IF OBJECT_ID (N'dbo.booking', N'U') IS NOT NULL
    DELETE FROM dbo.booking;
