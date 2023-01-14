mapboxgl.accessToken =
    "pk.eyJ1IjoiYXRzbWl0aGFyYyIsImEiOiJjbGJ5eGx0MXEwOXh2M3BtejBvNmUzM3VpIn0.6cxXNEwIUQeui42i9lbHEg";
    const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v11",
    center: [12.568, 55.6761],
    zoom: 14,
});

// VV airports code
let airports = [];

// Create a popup, but don't add it to the map yet.
const popup = new mapboxgl.Popup({
    closeButton: false,
});

const filterEl = document.getElementById("feature-filter");
const listingEl = document.getElementById("feature-listing");
const filterGroup = document.getElementById("filter-group");

function renderListings(features) {
    const empty = document.createElement("p");
    // Clear any existing listings
    listingEl.innerHTML = "";
    if (features.length) {
        for (const feature of features) {
            const itemLink = document.createElement("a");
            const label = `${feature.properties.name} (${feature.properties.abbrev})`;
            //itemLink.href = feature.properties.wikipedia;
            itemLink.href = `https://www.gbif.org/occurrence/${feature.properties.key}`;
            itemLink.target = "_blank";
            itemLink.textContent = label;
            itemLink.addEventListener("mouseover", () => {
                // Highlight corresponding feature on the map
                popup.setLngLat(feature.geometry.coordinates).setText(label).addTo(map);
            });
            listingEl.appendChild(itemLink);
        }

        // Show the filter input
        filterEl.parentNode.style.display = "block";
    } else if (features.length === 0 && filterEl.value !== "") {
        empty.textContent = "No results found";
        listingEl.appendChild(empty);
    } else {
        empty.textContent =
            "Use the polygon tool to select a region. Then Press 'Enter' to search...";
        listingEl.appendChild(empty);

        // Hide the filter input
        filterEl.parentNode.style.display = "none";

        // remove features filter
        map.setFilter("airport", ["has", "abbrev"]);
    }
}

function normalize(string) {
    return string.trim().toLowerCase();
}

function getUniqueFeatures(features, comparatorProperty) {
    const uniqueIds = new Set();
    const uniqueFeatures = [];
    for (const feature of features) {
        const id = feature.properties[comparatorProperty];
        if (!uniqueIds.has(id)) {
            uniqueIds.add(id);
            uniqueFeatures.push(feature);
        }
    }
    return uniqueFeatures;
}
// ^^ airports code

map.on("load", () => {
    // Disable default box zooming.
    map.boxZoom.disable();
    // Load GBIF Occurence Map Tiles
    map.addSource("maps-occurences", {
        type: "vector",
        tiles: ["https:api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}.mvt?"],
    });

    // Add GBIF Occurence Map Tiles Layer
    map.addLayer({
        id: "occurence",
        type: "circle",
        source: "maps-occurences",
        "source-layer": "occurrence",
        paint: {
            "circle-radius": 1.5,
            "circle-color": "#679602",
        },
        layout: {
            visibility: "visible",
        },
    });

    // Add 3D Buildings Layer
    map.addLayer({
        id: "3d-buildings-layer",
        source: "composite",
        "source-layer": "building",
        filter: ["==", "extrude", "true"],
        type: "fill-extrusion",
        minzoom: 15,
        paint: {
            "fill-extrusion-color": "#aaa",
            "fill-extrusion-height": [
                "interpolate",
                ["linear"],
                ["zoom"],
                15,
                0,
                15.05,
                ["get", "height"],
            ],
            "fill-extrusion-base": [
                "interpolate",
                ["linear"],
                ["zoom"],
                15,
                0,
                15.05,
                ["get", "min_height"],
            ],
            "fill-extrusion-opacity": 0.6,
        },
    });
    
    //Load Icon/Symbol Images from URL
    map.loadImage(
        "https://cdn.glitch.global/83e86ffc-5495-4dc6-a988-f4cfcfb14b31/1F344_color.png?v=1673530588031",
        (error, image) => {
            if (error) throw error;
            if (!map.hasImage("Fungi")) map.addImage("Fungi", image);
        }
    );

    map.loadImage(
        "https://cdn.glitch.global/83e86ffc-5495-4dc6-a988-f4cfcfb14b31/1F33F_color.png?v=1673530596322",
        (error, image) => {
            if (error) throw error;
            if (!map.hasImage("Plantae")) map.addImage("Plantae", image);
        }
    );

    map.loadImage(
        "https://cdn.glitch.global/83e86ffc-5495-4dc6-a988-f4cfcfb14b31/1F9AB_color.png?v=1673530602195",
        (error, image) => {
            if (error) throw error;
            if (!map.hasImage("Animalia")) map.addImage("Animalia", image);
        }
    );
    
    map.loadImage(
        "https://cdn.glitch.global/83e86ffc-5495-4dc6-a988-f4cfcfb14b31/E011_color.png?v=1673631942440",
        (error, image) => {
            if (error) throw error;
            if (!map.hasImage("Chromista")) map.addImage("Chromista", image);
        }
    );
  
    map.loadImage(
        "https://cdn.glitch.global/83e86ffc-5495-4dc6-a988-f4cfcfb14b31/1F9EB_color.png?v=1673700315309",
        (error, image) => {
            if (error) throw error;
            if (!map.hasImage("Bacteria")) map.addImage("Bacteria", image);
        }
    );  
  
    map.loadImage(
        "https://cdn.glitch.global/83e86ffc-5495-4dc6-a988-f4cfcfb14b31/2753_color.png?v=1673537140302",
        (error, image) => {
            if (error) throw error;
            if (!map.hasImage("Incertae Sedis")) map.addImage("Incertae Sedis", image);
        }
    );

    //Initialize Mapbox Draw GL
    const draw = new MapboxDraw({
        displayControlsDefault: false,
        // Selecting which mapbox-gl-draw control buttons to add to the map.
        controls: {
            polygon: true,
            point: true,
            trash: true,
        },
    });

    // Update Search when draw.create/delete/update events occur
    var newLayers = [];
    map.addControl(draw);
    map.on("draw.create", updateSearch);
    map.on("draw.delete", updateSearch);
    map.on("draw.update", updateSearch);
    //document.getElementById("debug").innerHTML = `<p>${map.getLayer('airport').type}</p>`;
    //document.getElementById("debug").innerHTML = `<p>${250}</p>`;


    // VV airports code
    // Reset features filter as the map starts moving
    map.on("movestart", () => {
        map.setFilter("airport", ["has", "abbrev"]);
    });

    // Update visible features when map stops moving
    map.on("moveend", () => {
        const features = map.queryRenderedFeatures({ layers: ["airport"] });
        if (features) {
            const uniqueFeatures = getUniqueFeatures(features, "key");
            renderListings(uniqueFeatures);
            filterEl.value = "";
            airports = uniqueFeatures;
        }
    });

    // Change the cursor style and populate the popup if hovering over POI
    map.on("mousemove", "airport", (e) => {
        map.getCanvas().style.cursor = "pointer";
        const feature = e.features[0];
        popup
            .setLngLat(feature.geometry.coordinates)
            .setText(`${feature.properties.name} (${feature.properties.abbrev})`)
            .addTo(map);
    });

    // Open feature webpage if POI is clicked
    map.on("mouseclick", "airport", (e) => {
        const feature = e.features[0];
        window.open(
            `https://www.gbif.org/occurrence/${feature.properties.key}`,
            "_blank"
        );
    });

    // Change the cursor style back after hover over POI
    map.on("mouseleave", "airport", () => {
        map.getCanvas().style.cursor = "";
        popup.remove();
    });

    // Filter visible features that match the input "filter" value and populate sidebar with results
    filterEl.addEventListener("keyup", (e) => {
        const value = normalize(e.target.value);
        const filtered = [];
        for (const feature of airports) {
            const name = normalize(feature.properties.name);
            const code = normalize(feature.properties.abbrev);
            if (name.includes(value) || code.includes(value)) {
                filtered.push(feature);
            }
        }

        // Populate the sidebar with filtered results
        renderListings(filtered);

        // Set the filter to populate features into the layer.
        if (filtered.length) {
            map.setFilter("airport", [
                "match",
                ["get", "abbrev"],
                filtered.map((feature) => {
                    return feature.properties.abbrev;
                }),
                true,
                false,
            ]);
        }
    });

    // Call this function on initialization...passing an empty array to render an empty state
    renderListings([]);
    // ^^ airports code

    // Convert a geoJSON polygon to a Well-Known-Text Polyogn
    function geoJSONToWKTPolygon(geoJSON) {
        if (geoJSON.type !== "FeatureCollection") {
            throw new Error("Input must be a GeoJSON FeatureCollection");
        }
        // Extract the first Polygon from the GeoJSON features
        const polygon = geoJSON.features.find((feature) => {
            if (feature.type !== "Feature") {
                throw new Error("GeoJSON features must be Feature objects");
            }
            return feature.geometry.type === "Polygon";
        });
        if (!polygon) {
            throw new Error("No Polygon found in the GeoJSON features");
        }
        // Convert the Polygon coordinates to WKT format
        const wktPoints = polygon.geometry.coordinates[0]
            .map((point) => `${point[0]} ${point[1]}`)
            .join(",");
        // Return the WKT Polygon string
        return `POLYGON((${wktPoints}))`;
    }

    // Convert Array of GBIF JSON pages into flattened GeoJSON format
    function jsonArrayToGeoJSONFeatures(jsonArray) {
        var features = [];
        for (let i = 0; i < jsonArray.length; i++) {
            features[i] = jsonArray[i].results.map((result) => {
                return {
                    type: "Feature",
                    geometry: {
                        type: "Point",
                        coordinates: [result.decimalLongitude, result.decimalLatitude],
                    },
                    properties: {
                        key: result.key,
                        kingdom: result.kingdom,
                        name: result.genericName,
                        abbrev: result.basisOfRecord,
                    },
                };
            });
        }
        return features.flat();
    }

    // Fetch JSON data from a URL
    async function getDataJSON(url) {
        try {
            let data = await fetch(url);
            return await data.json();
        } catch (error) {
            console.log(error);
        }
    }

    // Return the "count" property of JSON data
    async function renderCount(url) {
        let data = await getDataJSON(url);
        return data.count;
    }

    // Return an ordered list of
    function calcOffsets(integer) {
        let offsets = [];
        for (let i = 0; i < integer; i++) {
            offsets[i] = i * 300;
        }
        return offsets;
    }

    async function resolveResponseArray(users) {
        const jsons = [];
        for (let i = 0; i < users.length; i++) {
            jsons[i] = await users[i].json();
        }
    }

    // Request occurence data within a geoJSON polygon
    async function pageRequest(geoJSON) {
        const wktPoly = geoJSONToWKTPolygon(geoJSON);
        const api = "https://api.gbif.org/v1/occurrence/search?geometry=";
        const params300 = "&limit=300";
        const params1 = "&limit=1";
        let url = api + wktPoly + params1;
        let count = await renderCount(url);
        let nPages = Math.ceil(count / 300);

        if (nPages >= 990) {
            throw new Error("Request too Large");
        }

        let offsets = calcOffsets(nPages);
        var jsonArray;
        const pagePromises = offsets.map((offset) =>
            fetch(`${api}${wktPoly}${params300}&offset=${offset}`)
        );
        await Promise.all(pagePromises)
            .then((results) => Promise.all(results.map((r) => r.json())))
            .then((results) => {
                jsonArray = results;
            });

        var geoJSONFeatures = jsonArrayToGeoJSONFeatures(jsonArray);

        return {
            type: "FeatureCollection",
            features: geoJSONFeatures,
        };
    }

    // Update Polygon Search Status
    async function updateSearch(e) {
        var places;
        if (e.type == "draw.delete") {
            map.removeSource("airports");
            map.removeLayer("airport");
        } else if (e.type == "draw.create" || e.type == "draw.update") {
            var geoJSONpoly = draw.getAll();
            if (geoJSONpoly.features.length > 0) {
                const gbifGeoJSON = await pageRequest(geoJSONpoly);
                //const places = gbifGeoJSON;
                if (map.getSource("airports") == undefined) {
                    map.addSource("airports", {
                        type: "geojson",
                        data: gbifGeoJSON,
                    });
                } else {
                    map.getSource("airports").setData(gbifGeoJSON);
                }

                // Add flat layer of circles
                if (map.getLayer("airport") == undefined) {
                    map.addLayer({
                        id: "airport",
                        type: "circle",
                        source: "airports",
                        paint: {
                            "circle-radius": 2,
                            "circle-stroke-width": 1,
                            "circle-color": "red",
                            "circle-stroke-color": "white",
                        },
                    });
                } else {
                    map.addLayer("airport");
                }
                
                // VV Checkbox Filter
                for (const feature of gbifGeoJSON.features) {
                    const symbol = feature.properties.kingdom;
                    const layerID = `poi-${symbol}`;

                    // Add a layer for this symbol type if it hasn't been added already.
                    if (map.getLayer(layerID) == undefined) {
                        map.addLayer({
                            id: layerID,
                            type: "symbol",
                            source: "airports",
                            layout: {
                                "icon-image": `${symbol}`,
                                "icon-allow-overlap": true,
                                "icon-size": 0.05,
                            },
                            filter: ["==", "kingdom", symbol],
                        });
                        
                        
                        // Add checkbox and label elements for the layer.
                        const input = document.createElement("input");
                        input.type = "checkbox";
                        input.id = layerID;
                        input.checked = true;
                        filterGroup.appendChild(input);

                        const label = document.createElement("label");
                        label.setAttribute("for", layerID);
                        label.textContent = symbol;
                        filterGroup.appendChild(label);

                        // When the checkbox changes, update the visibility of the layer.
                        input.addEventListener("change", (e) => {
                            map.setLayoutProperty(
                                layerID,
                                "visibility",
                                e.target.checked ? "visible" : "none"
                            );
                        });
                    }
                }
            }
        }
    }
});
