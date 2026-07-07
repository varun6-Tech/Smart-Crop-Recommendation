
def get_crop_details(crop_name):
    '''
    Returns an extensive dictionary of details for a given crop.
    '''
    crop_info = {
        'rice': {
            'fertilizer': 'Urea',
            'water_req': 'High (100-150 cm)',
            'season': 'Kharif',
            'harvest_period': 'Winter (Nov - Dec)',
            'tips': 'Maintain proper irrigation.\nApply fertilizer in recommended quantity.\nRemove weeds regularly.',
            'soil_type': 'Clayey loam',
            'growth_duration': '120-150 Days',
            'avg_yield': '3-4 Tons/Hectare',
            'description': 'Rice is a staple cereal grain that requires high moisture and warm temperatures to thrive.',
            'farming_practices': 'Puddling the soil before transplanting helps retain water. System of Rice Intensification (SRI) can significantly increase yields.'
        },
        'wheat': {
            'fertilizer': 'DAP',
            'water_req': 'Medium (45-65 cm)',
            'season': 'Rabi',
            'harvest_period': 'Spring (Mar - May)',
            'tips': 'Ensure good drainage.\nControl weeds during early stages.\nMonitor for rust diseases.',
            'soil_type': 'Well-drained loam to clay loam',
            'growth_duration': '110-130 Days',
            'avg_yield': '3-3.5 Tons/Hectare',
            'description': 'Wheat is a major cereal crop globally, thriving in cool, moist weather during early growth and warm, dry weather for maturation.',
            'farming_practices': 'Zero tillage can save water and time. Ensure proper spacing to prevent fungal infections like rust.'
        },
        'cotton': {
            'fertilizer': 'NPK 20:20:20',
            'water_req': 'Medium (70-120 cm)',
            'season': 'Kharif',
            'harvest_period': 'Winter (Oct - Dec)',
            'tips': 'Protect from bollworms.\nRequires plenty of sunshine.\nKeep field weed-free.',
            'soil_type': 'Black cotton soil (Regur)',
            'growth_duration': '150-180 Days',
            'avg_yield': '1.5-2 Tons/Hectare',
            'description': 'Cotton is a crucial cash crop heavily dependent on deep, well-drained soils and clear sunny days.',
            'farming_practices': 'Crop rotation with legumes prevents soil depletion. Use pheromone traps to naturally manage bollworms.'
        },
        'maize': {
            'fertilizer': 'Ammonium Sulphate',
            'water_req': 'Medium (50-80 cm)',
            'season': 'Kharif',
            'harvest_period': 'Autumn (Sep - Nov)',
            'tips': 'Good drainage is essential.\nApply nitrogen in split doses.\nControl fall armyworm.',
            'soil_type': 'Well-drained alluvial or red loam',
            'growth_duration': '90-110 Days',
            'avg_yield': '2.5-3 Tons/Hectare',
            'description': 'Maize is a versatile crop grown in various climates, highly responsive to nitrogen and sensitive to waterlogging.',
            'farming_practices': 'Maintain strict weed control in the first 30 days. Split nitrogen applications maximize absorption.'
        },
        'sugarcane': {
            'fertilizer': 'Potash',
            'water_req': 'High (150-250 cm)',
            'season': 'All Year (Long Duration)',
            'harvest_period': 'Winter/Spring (Dec - Mar)',
            'tips': 'Needs deep plowing.\nRegular weeding is crucial.\nRequires heavy fertilization.',
            'soil_type': 'Deep rich loamy soil',
            'growth_duration': '10-18 Months',
            'avg_yield': '60-80 Tons/Hectare',
            'description': 'Sugarcane is a long-duration cash crop requiring heavy irrigation, deep soil preparation, and constant nutrient management.',
            'farming_practices': 'Trash mulching conserves moisture. Propping the canes prevents lodging during heavy winds.'
        },
        'groundnut': {
            'fertilizer': 'SSP',
            'water_req': 'Low to Medium (40-60 cm)',
            'season': 'Kharif',
            'harvest_period': 'Autumn (Sep - Oct)',
            'tips': 'Apply gypsum for better pod formation.\nAvoid waterlogging.\nControl leaf spot disease.',
            'soil_type': 'Sandy loam, well-drained',
            'growth_duration': '100-120 Days',
            'avg_yield': '1.5-2 Tons/Hectare',
            'description': 'Groundnut (peanut) is a legume crop that enriches the soil with nitrogen and requires loose soil for peg penetration.',
            'farming_practices': 'Gypsum application at the pegging stage is critical for pod development. Avoid late-season drought.'
        },
        'apple': {
            'fertilizer': 'NPK 10:10:10',
            'water_req': 'Medium (100-120 cm)',
            'season': 'Winter/Spring',
            'harvest_period': 'Late Summer/Autumn',
            'tips': 'Requires chilling hours.\nRegular pruning is necessary.\nMonitor for scab and aphids.',
            'soil_type': 'Well-drained loamy soil, slightly acidic',
            'growth_duration': 'Perennial Tree',
            'avg_yield': '15-20 Tons/Hectare',
            'description': 'Apple trees require specific chilling hours during dormancy to bloom properly and produce high yields.',
            'farming_practices': 'Strategic pruning opens the canopy to light. Netting can protect fruit from hail and bird damage.'
        },
        'banana': {
            'fertilizer': 'NPK and Potash',
            'water_req': 'High (120-220 cm)',
            'season': 'All Year',
            'harvest_period': 'All Year',
            'tips': 'Needs protection from strong winds.\nFrequent irrigation required.\nDesuckering is important.',
            'soil_type': 'Deep, rich, well-drained loam',
            'growth_duration': '11-14 Months',
            'avg_yield': '40-50 Tons/Hectare',
            'description': 'Banana is a fast-growing herbaceous plant that demands extremely high moisture and constant nutrient feeding.',
            'farming_practices': 'Desuckering maintains the mother plant\'s vigor. Propping is required when the bunch is heavy to prevent uprooting.'
        },
        'blackgram': {
            'fertilizer': 'DAP',
            'water_req': 'Low (30-40 cm)',
            'season': 'Kharif/Zaid',
            'harvest_period': 'Autumn/Summer',
            'tips': 'Treat seeds before sowing.\nWeed control in first 30 days.\nProtect from yellow mosaic virus.',
            'soil_type': 'Heavier soils, clay loams',
            'growth_duration': '70-90 Days',
            'avg_yield': '0.8-1.0 Tons/Hectare',
            'description': 'Blackgram is a short-duration protein-rich pulse crop that can tolerate brief periods of drought.',
            'farming_practices': 'Seed treatment with Rhizobium increases nitrogen fixation. Use yellow sticky traps for whitefly control.'
        },
        'chickpea': {
            'fertilizer': 'SSP and DAP',
            'water_req': 'Low (25-40 cm)',
            'season': 'Rabi',
            'harvest_period': 'Spring (Mar - Apr)',
            'tips': 'Avoid excess irrigation.\nTreat seeds with Rhizobium.\nProtect from pod borer.',
            'soil_type': 'Well-drained heavy soils',
            'growth_duration': '100-110 Days',
            'avg_yield': '1.0-1.5 Tons/Hectare',
            'description': 'Chickpea is a major winter pulse crop that is highly sensitive to waterlogging and excessive moisture.',
            'farming_practices': 'Nipping (plucking the apical buds) encourages lateral branching and significantly boosts pod yield.'
        },
        'coconut': {
            'fertilizer': 'NPK + Organic Manure',
            'water_req': 'High (150-200 cm)',
            'season': 'All Year',
            'harvest_period': 'All Year',
            'tips': 'Regular watering is essential.\nKeep root zone clean.\nApply fertilizers in circular trenches.',
            'soil_type': 'Sandy loam, coastal soils',
            'growth_duration': 'Perennial Tree',
            'avg_yield': '10,000-14,000 Nuts/Hectare',
            'description': 'Coconut palms thrive in humid tropical climates and require substantial fertilization to maintain nut production.',
            'farming_practices': 'Apply fertilizers in trenches 1.5m away from the trunk. Husk burial around the basin conserves moisture.'
        },
        'coffee': {
            'fertilizer': 'NPK Blends',
            'water_req': 'High (150-200 cm)',
            'season': 'Pre-monsoon',
            'harvest_period': 'Winter (Nov - Feb)',
            'tips': 'Requires shade trees.\nPrune regularly.\nControl coffee berry borer.',
            'soil_type': 'Deep, friable, porous soil rich in organic matter',
            'growth_duration': 'Perennial Bush',
            'avg_yield': '0.8-1.2 Tons/Hectare',
            'description': 'Coffee is a shade-loving plantation crop grown at higher altitudes with well-distributed rainfall.',
            'farming_practices': 'Maintain a two-tier shade canopy. Regular pruning of unproductive wood ensures better flowering.'
        },
        'grapes': {
            'fertilizer': 'Potassium-rich fertilizers',
            'water_req': 'Medium (50-90 cm)',
            'season': 'Winter',
            'harvest_period': 'Spring/Summer (Feb - Apr)',
            'tips': 'Training and pruning are critical.\nNeeds good drainage.\nProtect from powdery mildew.',
            'soil_type': 'Well-drained sandy to loamy soils',
            'growth_duration': 'Perennial Vine',
            'avg_yield': '20-30 Tons/Hectare',
            'description': 'Grapes require meticulous pruning and training on trellises. They are highly responsive to potassium for fruit sweetness.',
            'farming_practices': 'Bower or Y-trellis systems provide the best yields. Use timely copper sprays to manage downy mildew.'
        },
        'jute': {
            'fertilizer': 'Urea',
            'water_req': 'High (150-200 cm)',
            'season': 'Kharif',
            'harvest_period': 'Autumn (Jul - Oct)',
            'tips': 'Needs hot and humid climate.\nTimely weeding is crucial.\nProper retting is needed for good fiber.',
            'soil_type': 'Alluvial soil, loamy',
            'growth_duration': '120-150 Days',
            'avg_yield': '2-3 Tons/Hectare (Dry Fiber)',
            'description': 'Jute is a major bast fiber crop requiring hot, humid climates and plenty of clean water for the retting process.',
            'farming_practices': 'Maintain a plant population of 40-50 plants per sq meter. Retting in slow-moving clear water yields the best fiber color.'
        },
        'kidneybeans': {
            'fertilizer': 'NPK 15:15:15',
            'water_req': 'Medium (40-50 cm)',
            'season': 'Kharif',
            'harvest_period': 'Autumn',
            'tips': 'Ensure good drainage.\nAvoid working in wet fields to prevent disease spread.',
            'soil_type': 'Well-drained sandy loam',
            'growth_duration': '90-120 Days',
            'avg_yield': '1.0-1.2 Tons/Hectare',
            'description': 'Kidney beans (Rajma) are sensitive to waterlogging and require cool nights for proper grain filling.',
            'farming_practices': 'Avoid overhead irrigation to prevent foliar diseases. Use certified disease-free seeds.'
        },
        'lentil': {
            'fertilizer': 'DAP',
            'water_req': 'Low (20-30 cm)',
            'season': 'Rabi',
            'harvest_period': 'Spring (Feb - Apr)',
            'tips': 'Tolerant to drought.\nWeed management in early stages.\nTreat seeds before planting.',
            'soil_type': 'Light loams and alluvial soils',
            'growth_duration': '110-120 Days',
            'avg_yield': '1.0-1.5 Tons/Hectare',
            'description': 'Lentil is a hardy winter pulse crop that can survive on residual soil moisture with minimal irrigation.',
            'farming_practices': 'Ensure fine tilth before sowing. Pre-emergence herbicides are critical as lentils compete poorly with weeds early on.'
        },
        'mothbeans': {
            'fertilizer': 'SSP',
            'water_req': 'Very Low (15-25 cm)',
            'season': 'Kharif',
            'harvest_period': 'Autumn',
            'tips': 'Extremely drought tolerant.\nGrown in sandy soils.\nRequires minimal care.',
            'soil_type': 'Sandy and arid soils',
            'growth_duration': '60-70 Days',
            'avg_yield': '0.4-0.6 Tons/Hectare',
            'description': 'Moth bean is one of the most drought-resistant pulses, capable of growing in arid, sandy conditions where other crops fail.',
            'farming_practices': 'Can be broadcasted. Acts as an excellent cover crop to prevent soil erosion in desert fringes.'
        },
        'mungbean': {
            'fertilizer': 'DAP',
            'water_req': 'Low (30-40 cm)',
            'season': 'Zaid/Kharif',
            'harvest_period': 'Summer/Autumn',
            'tips': 'Short duration crop.\nGood for crop rotation.\nNeeds timely pest control.',
            'soil_type': 'Well-drained loams',
            'growth_duration': '60-70 Days',
            'avg_yield': '1.0-1.2 Tons/Hectare',
            'description': 'Mungbean is a rapid-growing pulse excellent for catching seasons between major crops, fixing nitrogen into the soil.',
            'farming_practices': 'Harvesting should be done when 80% of pods turn black. Seed treatment prevents early seedling blight.'
        },
        'muskmelon': {
            'fertilizer': 'NPK with high Potassium',
            'water_req': 'Medium (40-60 cm)',
            'season': 'Zaid',
            'harvest_period': 'Summer',
            'tips': 'Sandy loam soil is best.\nFrequent light irrigation.\nNeeds plenty of sunshine.',
            'soil_type': 'Sandy loam, well-drained',
            'growth_duration': '90-100 Days',
            'avg_yield': '15-20 Tons/Hectare',
            'description': 'Muskmelon is a warm-season vining crop that requires plenty of sunshine and potassium for sweetness.',
            'farming_practices': 'Withhold irrigation a few days before harvest to increase the sugar content of the fruit.'
        },
        'orange': {
            'fertilizer': 'NPK + Micronutrients',
            'water_req': 'Medium to High (90-110 cm)',
            'season': 'Monsoon',
            'harvest_period': 'Winter/Spring',
            'tips': 'Needs well-drained soil.\nRegular pruning required.\nMonitor for citrus canker.',
            'soil_type': 'Deep, well-drained loamy soils',
            'growth_duration': 'Perennial Tree',
            'avg_yield': '15-20 Tons/Hectare',
            'description': 'Oranges are subtropical citrus fruits highly susceptible to waterlogging. They require micronutrient sprays (Zn, Fe) for optimal health.',
            'farming_practices': 'Drip irrigation prevents root rot. Apply micronutrient foliar sprays during the active flush periods.'
        },
        'papaya': {
            'fertilizer': 'NPK',
            'water_req': 'Medium (100-120 cm)',
            'season': 'Monsoon/Spring',
            'harvest_period': 'All Year',
            'tips': 'Highly sensitive to waterlogging.\nProtect from frost.\nVirus control is critical.',
            'soil_type': 'Light to medium, extremely well-drained',
            'growth_duration': '9-14 Months',
            'avg_yield': '30-40 Tons/Hectare',
            'description': 'Papaya is a fast-growing tropical fruit that will die rapidly if water pools around its roots for even 24 hours.',
            'farming_practices': 'Grow on raised beds. Isolate fields from old infected papaya orchards to prevent Papaya Ring Spot Virus (PRSV).'
        },
        'pigeonpeas': {
            'fertilizer': 'DAP',
            'water_req': 'Medium (60-80 cm)',
            'season': 'Kharif',
            'harvest_period': 'Winter/Spring (Dec - Mar)',
            'tips': 'Deep rooted, drought tolerant.\nNeeds weed-free environment early on.\nProtect from pod borers.',
            'soil_type': 'Deep well-drained loams',
            'growth_duration': '150-180 Days',
            'avg_yield': '1.5-2.0 Tons/Hectare',
            'description': 'Pigeonpea (Tur) is a deep-rooted, drought-tolerant pulse often grown as an intercrop with cereals or cotton.',
            'farming_practices': 'Intercropping with short-duration crops (like mungbean) maximizes land use. Monitor strictly for Helicoverpa armigera during flowering.'
        },
        'pomegranate': {
            'fertilizer': 'NPK + Organic Manure',
            'water_req': 'Low to Medium (50-60 cm)',
            'season': 'Monsoon',
            'harvest_period': 'Autumn/Winter',
            'tips': 'Tolerates arid conditions.\nPruning is important.\nMaintain uniform soil moisture to prevent fruit cracking.',
            'soil_type': 'Light to medium well-drained soils',
            'growth_duration': 'Perennial Tree',
            'avg_yield': '12-15 Tons/Hectare',
            'description': 'Pomegranate is highly suited to arid and semi-arid regions, known for its high market value and hardiness.',
            'farming_practices': 'Maintain strict irrigation schedules during fruiting; sudden watering after dry spells causes the fruit to crack.'
        },
        'watermelon': {
            'fertilizer': 'NPK with high Potassium',
            'water_req': 'Medium (40-60 cm)',
            'season': 'Zaid',
            'harvest_period': 'Summer',
            'tips': 'Requires warm climate.\nSandy loam soil preferred.\nKeep fruits off wet soil.',
            'soil_type': 'Sandy and sandy loam',
            'growth_duration': '80-95 Days',
            'avg_yield': '25-30 Tons/Hectare',
            'description': 'Watermelon is a fast-growing summer crop that requires high temperatures and careful water management to prevent fungal diseases.',
            'farming_practices': 'Use plastic mulching to control weeds, conserve moisture, and keep the developing fruits clean and rot-free.'
        },
        'mango': {
            'fertilizer': 'NPK + Farm Yard Manure',
            'water_req': 'Medium (70-90 cm)',
            'season': 'Monsoon',
            'harvest_period': 'Summer (Apr - Jul)',
            'tips': 'Needs deep, well-drained soil.\nProtect young plants from frost/heat.\nPrune for better canopy management.',
            'soil_type': 'Deep well-drained laterite or alluvial',
            'growth_duration': 'Perennial Tree',
            'avg_yield': '8-10 Tons/Hectare',
            'description': 'Mango is the king of fruits, deeply rooted and capable of surviving extended dry periods once established.',
            'farming_practices': 'Paclobutrazol application can induce flowering in off-years. Center-opening pruning improves light penetration and fruit color.'
        }
    }
    
    # Default fallback
    default_info = {
        'fertilizer': 'Standard NPK',
        'water_req': 'Medium',
        'season': 'Varies',
        'harvest_period': 'Varies',
        'tips': 'Ensure balanced soil pH.\nRegular soil testing recommended.\nMonitor for local pests.',
        'soil_type': 'Loamy soil',
        'growth_duration': '90-120 Days',
        'avg_yield': 'Varies by region',
        'description': 'A versatile agricultural crop requiring standard nutrient and moisture management.',
        'farming_practices': 'Conduct routine soil testing. Implement crop rotation to prevent soil exhaustion.'
    }
    
    return crop_info.get(crop_name.lower(), default_info)


def get_fertilizer_details(fertilizer_name):
    '''
    Returns an extensive dictionary of details for a given fertilizer.
    '''
    # Normalize input
    fname = str(fertilizer_name).lower().strip()
    
    fert_db = {
        'urea': {
            'name': 'Urea (46% Nitrogen)',
            'application_method': 'Broadcasting or Top Dressing',
            'recommended_quantity': 'Varies strictly by crop; generally 50-100 kg/acre in splits.',
            'best_time': 'During active vegetative growth phases; avoid applying on totally dry soil.',
            'benefits': 'Provides an massive, rapid boost of Nitrogen to promote aggressive vegetative and leaf growth.',
            'precautions': 'Highly volatile. Should be incorporated into soil or watered in immediately to prevent ammonia volatilization. Can burn leaves if applied directly on wet foliage.'
        },
        'dap': {
            'name': 'Di-Ammonium Phosphate (DAP) (18% N, 46% P)',
            'application_method': 'Basal Application (Drilled into soil)',
            'recommended_quantity': '50 kg/acre at the time of sowing.',
            'best_time': 'At or just before sowing/planting as a basal dose.',
            'benefits': 'Provides critical Phosphorus for aggressive early root development and seedling establishment, alongside a starter dose of Nitrogen.',
            'precautions': 'Do not place directly in contact with seeds as the ammonia can cause seed toxicity. Drill below or to the side of the seed line.'
        },
        'ssp': {
            'name': 'Single Super Phosphate (SSP) (16% P, 11% S, 21% Ca)',
            'application_method': 'Basal Application',
            'recommended_quantity': '100-150 kg/acre depending on soil deficiency.',
            'best_time': 'Pre-planting or at the time of sowing.',
            'benefits': 'Excellent for oilseeds and legumes. Provides Phosphorus, Calcium, and Sulphur, improving pod formation and oil content.',
            'precautions': 'Slower release than DAP. Works best in neutral to alkaline soils. In highly acidic soils, it can become fixed.'
        },
        'potash': {
            'name': 'Muriate of Potash (MOP) (60% K)',
            'application_method': 'Basal or Split Top Dressing',
            'recommended_quantity': '20-40 kg/acre depending on crop.',
            'best_time': 'Split 50% at sowing, 50% during flowering/fruiting stage.',
            'benefits': 'Enhances disease resistance, improves drought tolerance, and drastically improves the size, color, and sweetness of fruits and grains.',
            'precautions': 'Contains chlorides, which can be toxic to sensitive crops like tobacco or certain vegetables in high doses.'
        },
        'ammonium sulphate': {
            'name': 'Ammonium Sulphate (21% N, 24% S)',
            'application_method': 'Top Dressing',
            'recommended_quantity': '40-60 kg/acre.',
            'best_time': 'Vegetative stage, especially for sulfur-loving crops.',
            'benefits': 'Acidifying effect lowers pH in alkaline soils. Ideal for crops like maize, onion, and garlic requiring high sulfur.',
            'precautions': 'Continuous use without lime can make soil highly acidic over time. Do not mix with alkaline materials.'
        },
        'npk 20:20:20': {
            'name': 'NPK 20:20:20 (Water Soluble)',
            'application_method': 'Foliar Spray or Fertigation',
            'recommended_quantity': '1-2 kg/acre via drip, or 5-10g per liter for spray.',
            'best_time': 'During critical growth stages (vegetative, flowering) for immediate nutrient correction.',
            'benefits': '100% water soluble. Delivers an immediate, perfectly balanced dose of major nutrients directly to the plant.',
            'precautions': 'Spray during early morning or late evening to prevent leaf scorch. Do not mix with incompatible agrochemicals.'
        },
        'npk 10:10:10': {
            'name': 'NPK 10:10:10 (Balanced Fertilizer)',
            'application_method': 'Basal or Top Dressing',
            'recommended_quantity': '50-100 kg/acre.',
            'best_time': 'Early growth stages.',
            'benefits': 'Provides a slow, steady, balanced supply of N, P, and K. Excellent for general garden crops and trees.',
            'precautions': 'Ensure even broadcasting. Water the field immediately after application if top-dressing.'
        },
        'npk 15:15:15': {
            'name': 'NPK 15:15:15',
            'application_method': 'Basal Application',
            'recommended_quantity': '50-80 kg/acre.',
            'best_time': 'Pre-planting.',
            'benefits': 'Slightly more concentrated balanced fertilizer, great for baseline soil fertility improvement.',
            'precautions': 'Store in a dry place as it can be hygroscopic.'
        }
    }
    
    # Simple keyword matching for default fallback
    for key, data in fert_db.items():
        if key in fname or fname in key:
            return data
            
    # Default fallback
    return {
        'name': fertilizer_name.title(),
        'application_method': 'Standard Basal or Top Dressing',
        'recommended_quantity': 'Based on local soil test recommendations.',
        'best_time': 'During active growth or pre-sowing.',
        'benefits': 'Supplies essential macro/micro nutrients to support robust plant growth and yield.',
        'precautions': 'Always test soil before mass application. Do not over-apply to prevent fertilizer burn and leaching.'
    }
