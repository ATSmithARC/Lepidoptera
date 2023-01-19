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
    public class LO_DeconstructFeatureCollection : GH_Component
    {
        public LO_DeconstructFeatureCollection()
            : base(nameof(LO_DeconstructFeatureCollection), "dFC", "Deconstruct a Lepidoptera FeatureCollection", "Lepidoptera", "Regional Analysis")
        {
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("FeatureCollection", "FC", "A Lepidoptera FeatureCollection to Deconstruct", GH_ParamAccess.item);
        }

        private static int IN_FeatureCollection = 0;
        private static int OUT_Features = 0;
        private static int OUT_Type = 1;
        private static int OUT_IsValid = 2;

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.AddGenericParameter("Features", "F", "A list of Lepidoptera Features", GH_ParamAccess.list);
            pManager.AddTextParameter("Type", "T", "The FeatureCollection Type", GH_ParamAccess.item);
            pManager.AddBooleanParameter("IsValid", "iV", "True if FeatureCollection is Valid", GH_ParamAccess.item);
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            LO_DeconstructFeatureCollection.DeonstructFeatureCollectionFromDA(DA);
        }

        protected override System.Drawing.Bitmap Icon => Resources.Lepidoptera;
        public override Guid ComponentGuid => new Guid("3ebe63a1-a2f3-40df-b136-33d271e2b07f");
        private static void DeonstructFeatureCollectionFromDA(IGH_DataAccess DA)
        {            
            FeatureCollectionGoo fcGoo = new FeatureCollectionGoo();

            if (!DA.GetData<Lepidoptera.FeatureCollectionGoo>(IN_FeatureCollection, ref fcGoo)) { return; }
            
            var featureGoos = new FeatureGoo[fcGoo.Value.features.Count];
            for (int i = 0; i < fcGoo.Value.features.Count; i++)
            {
                Feature feature = fcGoo.Value.features[i];
                FeatureGoo featureGoo = new FeatureGoo(feature);
                featureGoos[i] = featureGoo;
            }

            DA.SetDataList(OUT_Features, featureGoos);
            DA.SetData(OUT_Type, fcGoo.Value.type);
            DA.SetData(OUT_IsValid, fcGoo.Value.IsValid);

        }
    }
}