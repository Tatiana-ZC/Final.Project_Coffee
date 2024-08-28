CREATE TABLE coffee_trading_statistics 
SELECT
    Period,
    ReporterISO,
    ReporterDesc,
    CmdCode,
    CmdDesc,
    
    -- Total Calculations
    COUNT(DISTINCT CASE WHEN FlowCode = 'X' THEN PartnerISO END) AS Total_Export_Partners,
    COUNT(DISTINCT CASE WHEN FlowCode = 'M' THEN PartnerISO END) AS Total_Import_Partners,
    COUNT(DISTINCT PartnerISO) AS Total_Trade_Partners,
    
    SUM(CASE WHEN FlowCode = 'X' THEN Qty_in_kg ELSE 0 END) AS Total_Qty_Exported,
    SUM(CASE WHEN FlowCode = 'M' THEN Qty_in_kg ELSE 0 END) AS Total_Qty_Imported,
    SUM(CASE WHEN FlowCode = 'X' THEN PrimaryValue ELSE 0 END) AS Total_Value_Exported,
    SUM(CASE WHEN FlowCode = 'M' THEN PrimaryValue ELSE 0 END) AS Total_Value_Imported,
    
    -- Production Calculations
    (SUM(CASE WHEN FlowCode = 'X' THEN Qty_in_kg ELSE 0 END) - 
     SUM(CASE WHEN FlowCode = 'M' THEN Qty_in_kg ELSE 0 END)) AS Total_Production_Kg,
     
    (SUM(CASE WHEN FlowCode = 'X' THEN PrimaryValue ELSE 0 END) - 
     SUM(CASE WHEN FlowCode = 'M' THEN PrimaryValue ELSE 0 END)) AS Total_Production_Value,
    
    -- Average Calculations
    AVG(CASE WHEN FlowCode = 'X' THEN Qty_in_kg ELSE NULL END) AS Avg_Qty_Exported,
    AVG(CASE WHEN FlowCode = 'M' THEN Qty_in_kg ELSE NULL END) AS Avg_Qty_Imported,
    AVG(CASE WHEN FlowCode = 'X' THEN PrimaryValue ELSE NULL END) AS Avg_Value_Exported,
    AVG(CASE WHEN FlowCode = 'M' THEN PrimaryValue ELSE NULL END) AS Avg_Value_Imported,
    
    -- Production Average
    (AVG(CASE WHEN FlowCode = 'X' THEN Qty_in_kg ELSE NULL END) - 
     AVG(CASE WHEN FlowCode = 'M' THEN Qty_in_kg ELSE NULL END)) AS Avg_Production_Kg,
    
    (AVG(CASE WHEN FlowCode = 'X' THEN PrimaryValue ELSE NULL END) - 
     AVG(CASE WHEN FlowCode = 'M' THEN PrimaryValue ELSE NULL END)) AS Avg_Production_Value,
    
    -- Max Calculations
    MAX(CASE WHEN FlowCode = 'X' THEN Qty_in_kg ELSE NULL END) AS Max_Qty_Exported,
    MAX(CASE WHEN FlowCode = 'M' THEN Qty_in_kg ELSE NULL END) AS Max_Qty_Imported,
    MAX(CASE WHEN FlowCode = 'X' THEN PrimaryValue ELSE NULL END) AS Max_Value_Exported,
    MAX(CASE WHEN FlowCode = 'M' THEN PrimaryValue ELSE NULL END) AS Max_Value_Imported,
    
    -- Min Calculations
    MIN(CASE WHEN FlowCode = 'X' THEN Qty_in_kg ELSE NULL END) AS Min_Qty_Exported,
    MIN(CASE WHEN FlowCode = 'M' THEN Qty_in_kg ELSE NULL END) AS Min_Qty_Imported,
    MIN(CASE WHEN FlowCode = 'X' THEN PrimaryValue ELSE NULL END) AS Min_Value_Exported,
    MIN(CASE WHEN FlowCode = 'M' THEN PrimaryValue ELSE NULL END) AS Min_Value_Imported
    
FROM
    coffee_trading
GROUP BY
    Period,
    ReporterISO,
    ReporterDesc,
    CmdCode,
    CmdDesc
ORDER BY ReporterISO, Period, CmdCode;