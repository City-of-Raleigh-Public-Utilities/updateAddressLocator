#Monthly update for custom address locator used in geocoding 
#Created by Joe Zheng Li, PU GIS, joe.li@raleighnc.gov
import arcpy
import os, sys

#layer to include: Raleigh_MAR_Addresses, Raleigh_MAR_Streets, Wake_Property, Wake_Street
arcpy.env.overwriteOutput = True
filedir = "//corfile/Public_Utilities_NS/5215_Capital_Improvement_Projects/636_Geographic_Info_System/Joe/Geocoding"
geocodeWkspace = filedir + "/geocodingMaster.gdb"
RPUDwkspace = os.path.join(os.path.dirname(sys.argv[0]), r"RPUD_TESTDB.sde\RALEIGH.MAR")
WAKEwkspace = os.path.join(os.path.dirname(sys.argv[0]), "WAKE_PRODDB.sde")
# RPUDwkspace = "Database Connections/RPUD_TESTDB.sde/RALEIGH.MAR"
# WAKEwkspace = "Database Connections/WAKE_PRODDB.sde"

arcpy.env.workspace = filedir

if arcpy.Exists("geocodingMaster.gdb"):
    print "GDB exists! Overwriting file database..."
    arcpy.Delete_management(geocodeWkspace)
arcpy.CreateFileGDB_management(filedir, "geocodingMaster.gdb")
print "GDB created."

#Featureclass for creating address locator
RALEIGH_MAR_Streets = RPUDwkspace + "/RALEIGH.MAR_Streets"
RALEIGH_MAR_Addresses = RPUDwkspace + "/RALEIGH.MAR_Addresses"
WAKE_STREET = WAKEwkspace + "/WAKE.STREET"
WAKE_PROPERTY = WAKEwkspace + "/WAKE.PROPERTY_A_RECORDED"

#layer to address locator
arcpy.env.workspace = geocodeWkspace
print "Creating Address Locator from RALEIGH_MAR_Streets"
arcpy.CreateAddressLocator_geocoding("US Address - Dual Ranges", RALEIGH_MAR_Streets + " 'Primary table'", "'Feature ID' OBJECTID;'*From Left' FRLEFT;'*To Left' TOLEFT;'*From Right' FRRIGHT;'*To Right' TORIGHT;'Prefix Direction' <None>;'Prefix Type' <None>;'*Street Name' CARTONAME;'Suffix Type' <None>;'Suffix Direction' <None>;'Left City or Place' L_CITY;'Right City of Place' R_CITY;'Left ZIP Code' ZIP_L;'Right ZIP Code' ZIP_R;'Left State' STATE;'Right State' STATE", "MAR_Street_Locator", "", "DISABLED")
print "Creating Address Locator from WAKE_STREET"
arcpy.CreateAddressLocator_geocoding("US Address - Dual Ranges", WAKE_STREET + " 'Primary table'", "'Feature ID' OBJECTID;'*From Left' FRLEFT;'*To Left' TOLEFT;'*From Right' FRRIGHT;'*To Right' TORIGHT;'Prefix Direction' <None>;'Prefix Type' <None>;'*Street Name' CARTONAME;'Suffix Type' <None>;'Suffix Direction' <None>;'Left City or Place' L_ZIPNAME;'Right City of Place' R_ZIPNAME;'Left ZIP Code' ZIP_L;'Right ZIP Code' ZIP_R;'Left State' STATE;'Right State' STATE", "Wake_Street_Locator", "", "DISABLED")
print "Creating Address Locator from RALEIGH_MAR_Addresses"
arcpy.CreateAddressLocator_geocoding("US Address - Single House", RALEIGH_MAR_Addresses + " 'Primary table'", "'Feature ID' OBJECTID;'*House Number' ADDRNUM;'Side' <None>;'Prefix Direction' <None>;'Prefix Type' <None>;'*Street Name' STREETNAME;'Suffix Type' <None>;'Suffix Direction' <None>;'City or Place' CITY", "Mar_Addr_Locator", "", "DISABLED")
print "Creating Address Locator from WAKE_PROPERTY"
arcpy.CreateAddressLocator_geocoding("US Address - Single House", WAKE_PROPERTY + " 'Primary table'", "'Feature ID' OBJECTID;'*House Number' STNUM;'Side' <None>;'Prefix Direction' <None>;'Prefix Type' <None>;'*Street Name' FULL_STREET_NAME;'Suffix Type' <None>;'Suffix Direction' <None>;'City or Place' CITY_DECODE;'ZIP Code' ZIPNUM", "Wake_Property_Locator", "", "DISABLED")

#address locators to composite address locator
# AddrLocList = "Wake_Property_Locator Wake_Prop;MAR_Addr_Locator MAR_Addr;MAR_Street_Locator MAR_St;Wake_Street_Locator Wake_St"
print "Creating CopositeAddressLocator"
arcpy.CreateCompositeAddressLocator_geocoding(in_address_locators="Wake_Property_Locator Wake_Property;Mar_Addr_Locator Mar_Addr;MAR_Street_Locator MAR_Street;Wake_Street_Locator Wake_Street", in_field_map="""Street "Street or Intersection" true true true 100 Text 0 0 ,First,#,Wake_Property_Locator,Street,0,0,Mar_Addr_Locator,Street,0,0,MAR_Street_Locator,Street,0,0,Wake_Street_Locator,Street,0,0;City "City or Placename" true true false 40 Text 0 0 ,First,#,Wake_Property_Locator,City,0,0,Mar_Addr_Locator,City,0,0,MAR_Street_Locator,City,0,0,Wake_Street_Locator,City,0,0;State "State" true true false 20 Text 0 0 ,First,#,MAR_Street_Locator,State,0,0,Wake_Street_Locator,State,0,0;ZIP "ZIP Code" true true false 10 Text 0 0 ,First,#,Wake_Property_Locator,ZIP,0,0,MAR_Street_Locator,ZIP,0,0,Wake_Street_Locator,ZIP,0,0""", in_selection_criteria="Wake_Property #;Mar_Addr #;MAR_Street #;Wake_Street #", out_composite_address_locator="CompositeAddrLoc")