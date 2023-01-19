using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Lepidoptera;
using Lepidoptera_IO_Rhino;
using Lepidoptera_GHA.Properties;
using Newtonsoft.Json;
using System.IO;


namespace Lepidoptera_GHA
{
    public class LO_DeconstructS2Cell : GH_Component
    {
        public LO_DeconstructS2Cell()
            : base(nameof(LO_DeconstructS2Cell), "dS2", "Deconstruct a Lepidoptera S2Cell (Sentinal-2 Pixel)", "Lepidoptera", "Regional Analysis")
        {
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("S2Cell", "S2", "A Lepidoptera S2Cell to Deconstruct", GH_ParamAccess.item);
        }

        private static int IN_S2Cell = 0;
        private static int OUT_B1 = 0;
        private static int OUT_B2 = 1;
        private static int OUT_B3 = 2;
        private static int OUT_B4 = 3;
        private static int OUT_B5 = 4;
        private static int OUT_B6 = 5;
        private static int OUT_B7 = 6;
        private static int OUT_B8 = 7;
        private static int OUT_B8A = 8;
        private static int OUT_B9 = 9;
        private static int OUT_B11 = 10;
        private static int OUT_B12 = 11;
        private static int OUT_EVI = 12;
        private static int OUT_NDVI = 13;
        private static int OUT_SCL = 14;
        private static int OUT_TCI_R = 15;
        private static int OUT_TCI_G = 16;
        private static int OUT_TCI_B = 17;
        private static int OUT_WVP = 18;
        private static int OUT_bare = 19;
        private static int OUT_built = 20;
        private static int OUT_crops = 21;
        private static int OUT_flooded_vegitation = 22;
        private static int OUT_grass = 23;
        private static int OUT_label = 24;
        private static int OUT_shrub_and_scrub = 25;
        private static int OUT_snow_and_ice = 26;
        private static int OUT_trees = 27;
        private static int OUT_water = 28;
        private static int OUT_x = 29;
        private static int OUT_y = 30;

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.AddIntegerParameter("B1", "B1", "B1", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B2", "B2", "B2", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B3", "B3", "B3", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B4", "B4", "B4", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B5", "B5", "B5", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B6", "B6", "B6", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B7", "B7", "B7", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B8", "B8", "B8", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B8A", "B8A", "B8A", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B9", "B9", "B9", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B11", "B11", "B11", GH_ParamAccess.item);
            pManager.AddIntegerParameter("B12", "B12", "B12", GH_ParamAccess.item);
            pManager.AddNumberParameter("EVI", "EVI", "EVI", GH_ParamAccess.item);
            pManager.AddNumberParameter("NDVI", "NDVI", "NDVI", GH_ParamAccess.item);
            pManager.AddIntegerParameter("SCL", "SCL", "SCL", GH_ParamAccess.item);
            pManager.AddIntegerParameter("TCI_R", "TCI_R", "TCI_R", GH_ParamAccess.item);
            pManager.AddIntegerParameter("TCI_G", "TCI_G", "TCI_G", GH_ParamAccess.item);
            pManager.AddIntegerParameter("TCI_B", "TCI_B", "TCI_B", GH_ParamAccess.item);
            pManager.AddIntegerParameter("WVP", "WVP", "WVP", GH_ParamAccess.item);
            pManager.AddNumberParameter("bare", "bare", "bare", GH_ParamAccess.item);
            pManager.AddNumberParameter("built", "built", "built", GH_ParamAccess.item);
            pManager.AddNumberParameter("crops", "crops", "crops", GH_ParamAccess.item);
            pManager.AddNumberParameter("flooded_vegitation", "flooded_vegitation", "flooded_vegitation", GH_ParamAccess.item);
            pManager.AddNumberParameter("grass", "grass", "grass", GH_ParamAccess.item);
            pManager.AddIntegerParameter("label", "label", "label", GH_ParamAccess.item);
            pManager.AddNumberParameter("shrub_and_scrub", "shrub_and_scrub", "shrub_and_scrub", GH_ParamAccess.item);
            pManager.AddNumberParameter("snow_and_ice", "snow_and_ice", "snow_and_ice", GH_ParamAccess.item);
            pManager.AddNumberParameter("trees", "trees", "trees", GH_ParamAccess.item);
            pManager.AddNumberParameter("water", "water", "water", GH_ParamAccess.item);
            pManager.AddNumberParameter("x", "x", "x", GH_ParamAccess.item);
            pManager.AddNumberParameter("y", "y", "y", GH_ParamAccess.item);
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            LO_DeconstructS2Cell.DeonstructS2CellFromDA(DA);
        }

        protected override System.Drawing.Bitmap Icon => Resources.Lepidoptera;
        public override Guid ComponentGuid => new Guid("0dc7d4de-dca6-4953-a028-132a45cb4598");
        private static void DeonstructS2CellFromDA(IGH_DataAccess DA)
        {
            S2CellGoo s2Goo = new S2CellGoo();
            
            if (!DA.GetData<Lepidoptera.S2CellGoo>(IN_S2Cell, ref s2Goo)) { return; }
            S2Cell s2Cell = s2Goo.Value;
            DA.SetData(OUT_B1, s2Cell.B1);
            DA.SetData(OUT_B2, s2Cell.B2);
            DA.SetData(OUT_B3, s2Cell.B3);
            DA.SetData(OUT_B4, s2Cell.B4);
            DA.SetData(OUT_B5, s2Cell.B5);
            DA.SetData(OUT_B6, s2Cell.B6);
            DA.SetData(OUT_B7, s2Cell.B7);
            DA.SetData(OUT_B8, s2Cell.B8);
            DA.SetData(OUT_B8A, s2Cell.B8A);
            DA.SetData(OUT_B9, s2Cell.B9);
            DA.SetData(OUT_B11, s2Cell.B11);
            DA.SetData(OUT_B12, s2Cell.B12);
            DA.SetData(OUT_EVI, s2Cell.EVI);
            DA.SetData(OUT_NDVI, s2Cell.NDVI);
            DA.SetData(OUT_SCL, s2Cell.SCL);
            DA.SetData(OUT_TCI_R, s2Cell.TCI_R);
            DA.SetData(OUT_TCI_G, s2Cell.TCI_G);
            DA.SetData(OUT_TCI_B, s2Cell.TCI_B);
            DA.SetData(OUT_WVP, s2Cell.WVP);
            DA.SetData(OUT_bare, s2Cell.bare);
            DA.SetData(OUT_built, s2Cell.built);
            DA.SetData(OUT_crops, s2Cell.crops);
            DA.SetData(OUT_flooded_vegitation, s2Cell.flooded_vegitation);
            DA.SetData(OUT_grass, s2Cell.grass);
            DA.SetData(OUT_label, s2Cell.label);
            DA.SetData(OUT_shrub_and_scrub, s2Cell.shrub_and_scrub);
            DA.SetData(OUT_snow_and_ice, s2Cell.snow_and_ice);
            DA.SetData(OUT_trees, s2Cell.trees);
            DA.SetData(OUT_water, s2Cell.water);
            DA.SetData(OUT_x, s2Cell.x);
            DA.SetData(OUT_y, s2Cell.y);
        }
    }
}