IF OBJECT_ID (N'dbo.booking_dates', N'U') IS NOT NULL
    DROP TABLE dbo.booking_dates;

IF OBJECT_ID (N'dbo.booking', N'U') IS NOT NULL
    DROP TABLE dbo.booking;


CREATE TABLE dbo.booking (
    id VARCHAR(36) PRIMARY KEY,
    customer_name VARCHAR(100),
    created_date DATETIME2 NOT NULL DEFAULT GETDATE(),
	modified_date DATETIME2 NOT NULL DEFAULT GETDATE(),
);

CREATE TABLE dbo.booking_dates (
    id INT IDENTITY(1,1) PRIMARY KEY,
    booking_id VARCHAR(36) NOT NULL,
    date DATE NOT NULL,
    CONSTRAINT FK_booking_dates_bookings FOREIGN KEY (booking_id) 
        REFERENCES dbo.booking (id) ON DELETE CASCADE,

    CONSTRAINT UQ_booking_dates_date UNIQUE (date)
);
