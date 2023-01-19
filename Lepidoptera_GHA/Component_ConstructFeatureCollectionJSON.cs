using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Lepidoptera;
using Lepidoptera_IO_Rhino;
using Newtonsoft.Json;
using System.IO;
using Lepidoptera_GHA.Properties;

namespace Lepidoptera_GHA
{
    public class LO_FeatureCollectionFromJSON : GH_Component
    {
        public LO_FeatureCollectionFromJSON()
            : base(nameof(LO_FeatureCollectionFromJSON), "FCjson", "Construct a Lepidoptera FeatureCollection from JSON", "Lepidoptera", "Regional Analysis")
        {
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Path", "P", "TheFilePath of the JSON to Deserialize", GH_ParamAccess.item);
            pManager.AddBooleanParameter("Run", "R", "Set to True to Run", GH_ParamAccess.item, false);
        }

        private static int IN_Path = 0;
        private static int IN_Run = 1;
        private static int OUT_FeatureCollection = 0;

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.AddGenericParameter("FeatureCollection", "FC", "A Lepidoptera FeatureCollection", GH_ParamAccess.item);
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            LO_FeatureCollectionFromJSON.ConstructFeatureCollectionFromJSONFromDA(DA);
        }

        protected override System.Drawing.Bitmap Icon => Resources.Lepidoptera;
        public override Guid ComponentGuid => new Guid("5ac217b6-92c2-4775-9d38-09fdaded3628");
        private static void ConstructFeatureCollectionFromJSONFromDA(IGH_DataAccess DA)
        {
            string path = "";
            bool run = false;
            FeatureCollection fc = new FeatureCollection();
            
            if (!DA.GetData<bool>(IN_Run, ref run)) { return; } 
            if (!DA.GetData<string>(IN_Path, ref path)) { return; }
            if (run)
            {
                fc = FeatureCollection.FromJSON(path);
                FeatureCollectionGoo fcGoo = new FeatureCollectionGoo(fc);
                DA.SetData(OUT_FeatureCollection, fcGoo);
            }   
        }
    }
}