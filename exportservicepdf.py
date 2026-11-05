import arcpy

input_features = arcpy.GetParameterAsText(0)  # Selected Curb Stops FeatureSet
output_pdf_path = arcpy.GetParameterAsText(1) # Target PDF Output

aprx = arcpy.mp.ArcGISProject("CURRENT")
layout = aprx.listLayouts("ServiceLineReportLayout")[0]
map_frame = layout.listElements("MAPFRAME_ELEMENT")[0]

# Create a master PDF document
pdf_doc = arcpy.mp.PDFDocumentCreate(output_pdf_path)

# Iterate through each selected curb stop feature
with arcpy.da.SearchCursor(input_features, ["SHAPE@", "CurbStopID"]) as cursor:
    for row in cursor:
        geom, cs_id = row[0], row[1]
        
        # Center map frame on the individual curb stop
        map_frame.panToExtent(geom.extent)
        
        # Update text element
        for elem in layout.listElements("TEXT_ELEMENT"):
            if elem.name == "CurbStopIDText":
                elem.text = f"Curb Stop ID: {cs_id}"
        
        # Export temporary single page
        temp_page = f"{arcpy.env.scratchFolder}\\temp_{cs_id}.pdf"
        layout.exportToPDF(temp_page, resolution=300)
        
        # Append to master PDF
        pdf_doc.appendPages(temp_page)

pdf_doc.saveAndClose()
arcpy.SetParameterAsText(1, output_pdf_path)
