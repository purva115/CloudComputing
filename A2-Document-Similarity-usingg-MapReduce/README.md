# Assignment 2: Document Similarity using MapReduce

## Overview
This project implements a document similarity analysis using the MapReduce paradigm. It leverages Hadoop to process large datasets and compute similarity metrics between documents efficiently. The assignment demonstrates distributed computing concepts and practical use of Hadoop for text analytics.

## Features
- Distributed document similarity computation using MapReduce
- Hadoop integration via Docker
- Scalable for large datasets
- Modular code structure

## Prerequisites
- Docker and Docker Compose installed
- Java (for Hadoop)
- Basic knowledge of MapReduce and Hadoop

## Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Assignment2-Document-Similarity-usingg-MapReduce
   ```
2. **Start Hadoop using Docker Compose:**
   ```bash
   docker-compose up -d
   ```
3. **Configure Hadoop environment:**
   - Edit `hadoop.env` if needed for custom settings.
4. **Build the project:**
   ```bash
   mvn clean package
   ```

## Usage
1. **Prepare your input data:**
   - Place your text files in the appropriate HDFS directory.
2. **Run the MapReduce job:**
   - Submit your job to Hadoop using the built JAR file.
3. **View results:**
   - Output will be available in the specified HDFS output directory.

## Project Structure
- `src/main/`: Java source code for MapReduce jobs
- `docker-compose.yml`: Docker setup for Hadoop
- `hadoop.env`: Hadoop environment variables
- `pom.xml`: Maven build configuration
- `README.md`: Project documentation

---

## Approach and Implementation

### Mapper Design
The Mapper reads each line from the input dataset, where each line represents a document with a unique identifier and its content. The input key-value pair is typically the line offset and the line text. The Mapper tokenizes the document content into words and emits key-value pairs representing document-word relationships. For document similarity, the Mapper may also generate all possible document pairs and their associated word sets. This helps in preparing the data for pairwise comparison in the Reducer.

### Reducer Design
The Reducer receives document pairs as keys and lists of word sets as values. It processes these values to compute the intersection and union of word sets for each document pair. The final output is the document pair and their Jaccard Similarity, calculated as:

    Jaccard Similarity = (Number of common words) / (Total unique words)

The Reducer emits the document pair and their similarity score as the final output.

### Overall Data Flow
1. Input files are read line by line by the Mapper.
2. The Mapper emits key-value pairs for document pairs and their word sets.
3. During the shuffle and sort phase, all values for the same document pair are grouped together.
4. The Reducer processes each group, calculates the Jaccard Similarity, and emits the result.
5. The output is written to HDFS for retrieval.

## Challenges and Solutions
- **Pair Generation:** Generating all unique document pairs efficiently was challenging. This was solved by using appropriate data structures and logic in the Mapper.
- **Debugging in Hadoop:** Debugging distributed jobs can be difficult. Used logging and small test datasets to verify correctness.
- **Data Transfer:** Moving data between local, Docker, and HDFS required careful command usage and path management.
- **Output Directory Errors:** Hadoop jobs fail if the output directory exists. Changed output directory names to avoid errors.

## Setup and Execution
**Note:** Edit the commands as needed for your assignment.

1. **Start the Hadoop Cluster**
   ```bash
   docker compose up -d
   ```
2. **Build the Code**
   ```bash
   mvn clean package
   ```
3. **Copy JAR to Docker Container**
   ```bash
   docker cp target/WordCountUsingHadoop-0.0.1-SNAPSHOT.jar resourcemanager:/opt/hadoop-3.2.1/share/hadoop/mapreduce/
   ```
4. **Move Dataset to Docker Container**
   ```bash
   docker cp shared-folder/input/data/input.txt resourcemanager:/opt/hadoop-3.2.1/share/hadoop/mapreduce/
   ```
5. **Connect to Docker Container**
   ```bash
   docker exec -it resourcemanager /bin/bash
   cd /opt/hadoop-3.2.1/share/hadoop/mapreduce/
   ```
6. **Set Up HDFS**
   ```bash
   hadoop fs -mkdir -p /input/data
   hadoop fs -put ./input.txt /input/data
   ```
7. **Execute the MapReduce Job**
   ```bash
   hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/WordCountUsingHadoop-0.0.1-SNAPSHOT.jar com.example.controller.Controller /input/data/input.txt /output1
   ```
   *(Change output folder name if it already exists)*
8. **View the Output**
   ```bash
   hadoop fs -cat /output1/*
   ```
9. **Copy Output from HDFS to Local OS**
   ```bash
   hdfs dfs -get /output1 /opt/hadoop-3.2.1/share/hadoop/mapreduce/
   exit
   docker cp resourcemanager:/opt/hadoop-3.2.1/share/hadoop/mapreduce/output1/ shared-folder/output/
   ```
10. **Commit and Push**
    Commit and push your results to the repository.

## Sample Input
**Input from small_dataset.txt [1000 words]**
```
Document1 Cloud computing represents a fundamental shift in how organizations deploy and manage their information technology infrastructure enabling businesses to access computing resources including servers storage databases networking software analytics and intelligence over the internet through cloud service providers rather than owning and maintaining physical data centers and servers companies can rent access to anything from applications to storage from cloud service providers the benefits of cloud computing include cost reduction scalability flexibility reliability and security organizations can scale up or down their computing resources based on demand without significant upfront investments in hardware cloud providers offer various service models including Infrastructure as a Service Platform as a Service and Software as a Service each catering to different business needs and technical requirements public clouds provide shared infrastructure while private clouds offer dedicated resources for enhanced security and control hybrid clouds combine both approaches allowing organizations to optimize workload placement based on security performance and cost considerations multi-cloud strategies involve using multiple cloud providers to avoid vendor lock-in and optimize specialized services cloud migration involves moving existing applications and data from on-premises infrastructure to cloud environments requiring careful planning assessment and execution cloud native applications are designed specifically for cloud environments utilizing microservices containerization and DevOps practices to achieve maximum scalability and resilience

Document2 Machine learning has revolutionized the way we approach data analysis and pattern recognition across multiple industries this branch of artificial intelligence enables computers to learn and improve their performance on specific tasks without being explicitly programmed for each scenario machine learning algorithms can identify complex patterns in large datasets that would be impossible for humans to detect manually the three main types of machine learning are supervised learning unsupervised learning and reinforcement learning supervised learning uses labeled training data to make predictions on new unseen data unsupervised learning finds hidden patterns in data without labeled examples reinforcement learning involves agents learning optimal actions through trial and error interactions with their environment applications include recommendation systems fraud detection image recognition natural language processing and autonomous vehicles deep learning networks use multiple layers to process information hierarchically extracting increasingly complex features from raw input data convolutional neural networks excel at image processing tasks while recurrent neural networks handle sequential data such as natural language and time series feature engineering involves selecting and transforming input variables to improve model performance cross-validation techniques provide robust estimates of model performance by training and testing on different subsets of available data

Document3 Data science combines statistical analysis programming skills and domain expertise to extract meaningful insights from structured and unstructured data modern data scientists must be proficient in programming languages such as Python R SQL and Java while also understanding statistical concepts machine learning algorithms and data visualization techniques the data science process typically involves data collection cleaning exploration analysis modeling and interpretation of results data scientists work with various types of data including numerical categorical text images audio and video data they use tools like Jupyter notebooks pandas numpy matplotlib scikit-learn and TensorFlow to manipulate analyze and model data the field requires strong problem-solving skills critical thinking abilities and effective communication skills to translate complex technical findings into actionable business recommendations for stakeholders and decision makers statistical methods form the foundation of data analysis while programming enables automation and scalability data visualization plays crucial role in making complex analytical results accessible and understandable to stakeholders across different levels of technical expertise exploratory data analysis helps identify patterns trends and anomalies in datasets before applying advanced modeling techniques hypothesis testing validates assumptions and ensures statistical significance of findings

Document4 Big data refers to extremely large datasets that cannot be processed using traditional data processing applications due to their volume velocity and variety the three Vs of big data volume velocity and variety represent the core characteristics that distinguish big data from conventional data processing scenarios volume refers to the massive amounts of data generated every second from sources like social media sensors mobile devices and online transactions velocity describes the speed at which new data is generated and must be processed to remain relevant and useful variety encompasses the different types and formats of data including structured semi-structured and unstructured data from diverse sources organizations use big data analytics to gain competitive advantages improve operational efficiency enhance customer experiences and drive innovation through data-driven decision making processes Apache Hadoop and Spark are popular frameworks for distributed processing of big data across clusters of computers MapReduce programming model enables parallel processing of large datasets by dividing work into smaller tasks NoSQL databases provide scalable storage solutions for big data applications real-time analytics capabilities allow organizations to process and analyze streaming data as it arrives enabling immediate responses to changing conditions and emerging opportunities data lakes store vast amounts of raw data in native formats until needed for analysis

Document5 Database management systems serve as the foundation for storing organizing and retrieving vast amounts of information in modern computing environments these systems provide structured approaches to data storage ensuring data integrity consistency and accessibility across multiple users and applications simultaneously relational databases use structured query language SQL to manage data stored in tables with rows and columns connected through relationships and foreign keys NoSQL databases offer alternative approaches for handling unstructured and semi-structured data including document stores key-value pairs column-family databases and graph databases database administrators must ensure optimal performance through indexing query optimization backup and recovery procedures security measures and regular maintenance activities proper database design involves normalization entity-relationship modeling and careful consideration of data types constraints and relationships between different entities and attributes modern databases support ACID properties ensuring atomicity consistency isolation and durability of transactions database replication provides high availability through synchronous and asynchronous copying of data across multiple instances distributed databases enable horizontal scaling by partitioning data across multiple servers or geographic locations in-memory databases store data in RAM for extremely fast access times while traditional disk-based databases provide persistent storage solutions
```

## Sample Output
**Output from small_dataset.txt**
```
Document5, Document4	Similarity: 0.14
Document5, Document3	Similarity: 0.10
Document5, Document2	Similarity: 0.10
Document5, Document1	Similarity: 0.13
Document4, Document3	Similarity: 0.13
Document4, Document2	Similarity: 0.15
Document4, Document1	Similarity: 0.09
Document3, Document2	Similarity: 0.13
Document3, Document1	Similarity: 0.07
Document2, Document1	Similarity: 0.11

```
**Input from medium_dataset.txt [3000 words]**
```
Document1 Quantum computing represents a revolutionary paradigm shift from classical computing by leveraging quantum mechanical phenomena such as superposition entanglement and quantum interference to process information in fundamentally different ways. Unlike classical bits that exist in definite states of zero or one quantum bits or qubits can exist in superposition states representing both zero and one simultaneously until measured. This property enables quantum computers to explore multiple computational paths in parallel potentially solving certain complex problems exponentially faster than classical computers including cryptography optimization machine learning and scientific simulation applications.
Document2 Renewable energy technologies including solar photovoltaic wind power hydroelectric geothermal and biomass systems provide sustainable alternatives to fossil fuel consumption while reducing greenhouse gas emissions and environmental degradation. Solar panels convert sunlight directly into electricity through photovoltaic cells while wind turbines harness kinetic energy from moving air masses to generate power. Energy storage systems including lithium-ion batteries pumped hydro storage and emerging technologies like hydrogen fuel cells address intermittency challenges enabling grid stability and reliable power delivery from renewable sources across diverse geographic and climatic conditions.
Document3 Biotechnology and genetic engineering techniques manipulate biological systems and organisms to develop new products processes and applications for medicine agriculture environmental remediation and industrial manufacturing. CRISPR-Cas9 gene editing technology allows precise modification of DNA sequences enabling potential treatments for genetic diseases improved crop yields enhanced nutritional content and biofuel production. Synthetic biology combines engineering principles with biological design to create artificial biological systems and organisms with novel functions for pharmaceutical production environmental cleanup and sustainable manufacturing processes.
Document4 Space exploration and aerospace engineering advance human understanding of the universe while developing technologies for satellite communications navigation weather monitoring and planetary exploration. Rockets spacecraft and robotic probes enable scientific missions to study celestial bodies atmospheric conditions and cosmic phenomena providing insights into planetary formation stellar evolution and the potential for extraterrestrial life. Commercial space companies private partnerships and international collaborations expand access to space through reusable launch vehicles satellite constellations and planned missions to Mars and beyond.
Document5 Environmental sustainability practices focus on conservation renewable resources waste reduction and ecosystem preservation to maintain ecological balance for future generations. Circular economy principles emphasize reuse recycling and regenerative design to minimize resource consumption and environmental impact across manufacturing distribution and disposal processes. Climate change mitigation strategies include carbon sequestration renewable energy adoption sustainable transportation systems and policy frameworks promoting environmental stewardship and responsible resource management at local national and global scales.
Document6 Financial technology fintech innovations transform banking payments lending investment management and insurance services through digital platforms mobile applications and automated systems. Blockchain cryptocurrency decentralized finance and digital wallets provide alternative financial infrastructure enabling peer-to-peer transactions cross-border payments and programmable money without traditional intermediaries. Artificial intelligence machine learning and data analytics enhance risk assessment fraud detection algorithmic trading and personalized financial services while regulatory frameworks evolve to address security privacy and consumer protection concerns.
Document7 Educational technology e-learning platforms and digital learning environments expand access to knowledge and skills development through online courses virtual classrooms and interactive educational content. Personalized learning adaptive assessment systems and artificial intelligence tutoring provide customized educational experiences tailored to individual learning styles preferences and progress rates. Virtual reality augmented reality and immersive simulations create engaging educational experiences for complex subjects including science medicine engineering and history while addressing accessibility challenges and geographic barriers to quality education.
Document8 Healthcare informatics electronic health records telemedicine and medical devices integrate technology with patient care to improve diagnosis treatment outcomes and healthcare delivery efficiency. Wearable sensors remote monitoring systems and mobile health applications enable continuous health tracking preventive care and early intervention for chronic conditions. Artificial intelligence diagnostic imaging precision medicine and genomic analysis enhance clinical decision-making drug discovery and personalized treatment protocols while addressing privacy security and ethical considerations in healthcare data management.
Document9 Urban planning smart cities and sustainable infrastructure development address population growth environmental challenges and quality of life improvements in metropolitan areas. Intelligent transportation systems traffic management renewable energy grids and IoT sensors optimize resource utilization reduce congestion and enhance public services. Green building design sustainable architecture and urban agriculture promote environmental sustainability while addressing housing affordability social equity and community resilience in rapidly growing urban populations worldwide.
Document10 Manufacturing automation robotics and Industry 4.0 technologies transform production processes through cyber-physical systems digital twins and intelligent manufacturing networks. Advanced materials nanotechnology and additive manufacturing including 3D printing enable customized production lightweight structures and novel material properties for aerospace automotive electronics and medical applications. Supply chain optimization predictive maintenance and quality control systems enhance efficiency reduce costs and improve product reliability while addressing sustainability environmental impact and worker safety considerations.
Document11 Telecommunications networks 5G wireless technology and fiber optic infrastructure enable high-speed data transmission global connectivity and emerging applications including autonomous vehicles smart devices and IoT ecosystems. Network security protocols encryption standards and cybersecurity measures protect digital communications against unauthorized access data breaches and cyber attacks. Software-defined networking cloud computing and edge computing architectures provide scalable flexible infrastructure supporting diverse applications from social media to scientific research and business operations.
Document12 Agricultural technology precision farming and sustainable food production systems address global food security challenges while minimizing environmental impact and resource consumption. GPS-guided tractors drone monitoring soil sensors and automated irrigation systems optimize crop yields reduce chemical inputs and conserve water resources. Vertical farming hydroponics and controlled environment agriculture enable food production in urban areas with limited land while addressing climate change impacts on traditional farming practices.
Document13 Transportation systems autonomous vehicles electric mobility and sustainable logistics networks transform how people and goods move while addressing environmental concerns and urban congestion. Electric vehicle charging infrastructure battery technology and renewable energy integration support the transition from fossil fuel dependence toward cleaner transportation alternatives. Autonomous driving systems artificial intelligence and sensor technologies promise improved safety reduced traffic accidents and enhanced mobility access for elderly and disabled populations.
Document14 Materials science nanotechnology and advanced manufacturing techniques develop new materials with enhanced properties for applications in electronics energy storage medical devices and structural engineering. Carbon nanotubes graphene metamaterials and smart materials exhibit unique mechanical electrical and optical properties enabling innovations in computing renewable energy biomedical implants and aerospace applications. Research in materials characterization computational modeling and synthesis methods accelerates discovery and development of next-generation materials.
Document15 Cognitive science neuroscience and brain-computer interfaces explore the mechanisms of human cognition memory learning and consciousness while developing technologies to enhance human capabilities and treat neurological conditions. Neural prosthetics brain stimulation techniques and neurofeedback systems offer therapeutic applications for paralysis depression epilepsy and other neurological disorders. Research in artificial neural networks deep learning and cognitive architectures advances both understanding of biological intelligence and development of artificial intelligence systems.
Document16 Energy storage systems battery technologies and power grid modernization address renewable energy integration reliability and efficiency challenges in electrical distribution networks. Advanced battery chemistries including solid-state batteries flow batteries and supercapacitors provide improved energy density safety and longevity for applications from mobile devices to grid-scale storage. Smart grid technologies demand response systems and energy management platforms optimize electricity distribution reduce waste and accommodate distributed renewable energy sources.
Document17 Water management systems desalination technologies and environmental remediation address water scarcity pollution and ecosystem degradation challenges affecting global populations and environmental health. Advanced filtration reverse osmosis and atmospheric water generation provide clean drinking water in water-stressed regions while wastewater treatment systems protect environmental quality. Hydroponic systems water recycling and conservation practices promote sustainable water use in agriculture industry and urban development.
Document18 Pharmaceutical research drug discovery and personalized medicine advance healthcare through targeted therapies precision treatments and improved clinical outcomes for patients with diverse medical conditions. Computational drug design biomarker identification and clinical trial optimization accelerate development of safe effective medications while reducing costs and time-to-market. Regenerative medicine stem cell therapy and tissue engineering offer potential treatments for previously incurable conditions while addressing ethical considerations and regulatory requirements.
Document19 Disaster preparedness emergency response systems and resilience planning protect communities from natural disasters climate change impacts and human-caused emergencies through early warning systems evacuation planning and recovery coordination. Remote sensing satellites weather monitoring and predictive modeling enable accurate forecasting and risk assessment for hurricanes earthquakes floods and other hazardous events. Communication networks backup power systems and community preparedness programs ensure continued operation of critical infrastructure during emergencies.
Document20 Food science nutrition and sustainable agriculture practices address global nutrition challenges while promoting environmental sustainability and food system resilience. Plant-based proteins alternative meat products and nutritional enhancement techniques provide healthy sustainable food options while reducing environmental impact of traditional livestock production. Food safety systems traceability technologies and quality control measures ensure safe nutritious food supply chains from farm to consumer while addressing food waste and distribution challenges.
```
**Output from medium_dataset.txt**
```
Document14, Document15	Similarity: 0.10
Document14, Document12	Similarity: 0.03
Document14, Document13	Similarity: 0.05
Document14, Document10	Similarity: 0.11
Document14, Document11	Similarity: 0.06
Document14, Document20	Similarity: 0.04
Document14, Document9	Similarity: 0.07
Document14, Document8	Similarity: 0.08
Document14, Document7	Similarity: 0.05
Document14, Document6	Similarity: 0.04
Document14, Document5	Similarity: 0.06
Document14, Document4	Similarity: 0.05
Document14, Document3	Similarity: 0.13
Document14, Document2	Similarity: 0.05
Document14, Document1	Similarity: 0.06
Document14, Document18	Similarity: 0.11
Document14, Document19	Similarity: 0.04
Document14, Document16	Similarity: 0.12
Document14, Document17	Similarity: 0.04
Document15, Document12	Similarity: 0.04
Document15, Document13	Similarity: 0.09
Document15, Document10	Similarity: 0.08
Document15, Document11	Similarity: 0.06
Document15, Document20	Similarity: 0.08
Document15, Document9	Similarity: 0.07
Document15, Document8	Similarity: 0.11
Document15, Document7	Similarity: 0.10
Document15, Document6	Similarity: 0.09
Document15, Document5	Similarity: 0.04
Document15, Document4	Similarity: 0.11
Document15, Document3	Similarity: 0.09
Document15, Document2	Similarity: 0.05
Document15, Document1	Similarity: 0.07
Document15, Document18	Similarity: 0.08
Document15, Document19	Similarity: 0.06
Document15, Document16	Similarity: 0.09
Document15, Document17	Similarity: 0.07
Document12, Document13	Similarity: 0.08
Document12, Document10	Similarity: 0.09
Document12, Document11	Similarity: 0.05
Document12, Document20	Similarity: 0.16
Document12, Document9	Similarity: 0.17
Document12, Document8	Similarity: 0.12
Document12, Document7	Similarity: 0.06
Document12, Document6	Similarity: 0.07
Document12, Document5	Similarity: 0.13
Document12, Document4	Similarity: 0.04
Document12, Document3	Similarity: 0.10
Document12, Document2	Similarity: 0.07
Document12, Document1	Similarity: 0.02
Document12, Document18	Similarity: 0.05
Document12, Document19	Similarity: 0.07
Document12, Document16	Similarity: 0.07
Document12, Document17	Similarity: 0.15
Document13, Document10	Similarity: 0.10
Document13, Document11	Similarity: 0.07
Document13, Document20	Similarity: 0.09
Document13, Document9	Similarity: 0.14
Document13, Document8	Similarity: 0.07
Document13, Document7	Similarity: 0.08
Document13, Document6	Similarity: 0.08
Document13, Document5	Similarity: 0.07
Document13, Document4	Similarity: 0.06
Document13, Document3	Similarity: 0.09
Document13, Document2	Similarity: 0.11
Document13, Document1	Similarity: 0.02
Document13, Document18	Similarity: 0.05
Document13, Document19	Similarity: 0.06
Document13, Document16	Similarity: 0.13
Document13, Document17	Similarity: 0.09
Document10, Document11	Similarity: 0.05
Document10, Document20	Similarity: 0.13
Document10, Document9	Similarity: 0.09
Document10, Document8	Similarity: 0.11
Document10, Document7	Similarity: 0.09
Document10, Document6	Similarity: 0.07
Document10, Document5	Similarity: 0.07
Document10, Document4	Similarity: 0.06
Document10, Document3	Similarity: 0.08
Document10, Document2	Similarity: 0.06
Document10, Document1	Similarity: 0.03
Document10, Document18	Similarity: 0.09
Document10, Document19	Similarity: 0.06
Document10, Document16	Similarity: 0.12
Document10, Document17	Similarity: 0.08
Document11, Document20	Similarity: 0.06
Document11, Document9	Similarity: 0.05
Document11, Document8	Similarity: 0.08
Document11, Document7	Similarity: 0.06
Document11, Document6	Similarity: 0.08
Document11, Document5	Similarity: 0.03
Document11, Document4	Similarity: 0.06
Document11, Document3	Similarity: 0.04
Document11, Document2	Similarity: 0.06
Document11, Document1	Similarity: 0.06
Document11, Document18	Similarity: 0.03
Document11, Document19	Similarity: 0.06
Document11, Document16	Similarity: 0.09
Document11, Document17	Similarity: 0.04
Document20, Document9	Similarity: 0.14
Document20, Document8	Similarity: 0.05
Document20, Document7	Similarity: 0.09
Document20, Document6	Similarity: 0.09
Document20, Document5	Similarity: 0.12
Document20, Document4	Similarity: 0.05
Document20, Document3	Similarity: 0.11
Document20, Document2	Similarity: 0.11
Document20, Document1	Similarity: 0.03
Document20, Document18	Similarity: 0.06
Document20, Document19	Similarity: 0.06
Document20, Document16	Similarity: 0.12
Document20, Document17	Similarity: 0.15
Document9, Document8	Similarity: 0.07
Document9, Document7	Similarity: 0.06
Document9, Document6	Similarity: 0.07
Document9, Document5	Similarity: 0.10
Document9, Document4	Similarity: 0.04
Document9, Document3	Similarity: 0.07
Document9, Document2	Similarity: 0.08
Document9, Document1	Similarity: 0.02
Document9, Document18	Similarity: 0.06
Document9, Document19	Similarity: 0.07
Document9, Document16	Similarity: 0.11
Document9, Document17	Similarity: 0.17
Document8, Document7	Similarity: 0.10
Document8, Document6	Similarity: 0.14
Document8, Document5	Similarity: 0.04
Document8, Document4	Similarity: 0.06
Document8, Document3	Similarity: 0.08
Document8, Document2	Similarity: 0.05
Document8, Document1	Similarity: 0.03
Document8, Document18	Similarity: 0.17
Document8, Document19	Similarity: 0.06
Document8, Document16	Similarity: 0.10
Document8, Document17	Similarity: 0.07
Document7, Document6	Similarity: 0.13
Document7, Document5	Similarity: 0.03
Document7, Document4	Similarity: 0.07
Document7, Document3	Similarity: 0.09
Document7, Document2	Similarity: 0.08
Document7, Document1	Similarity: 0.04
Document7, Document18	Similarity: 0.09
Document7, Document19	Similarity: 0.05
Document7, Document16	Similarity: 0.08
Document7, Document17	Similarity: 0.07
Document6, Document5	Similarity: 0.04
Document6, Document4	Similarity: 0.03
Document6, Document3	Similarity: 0.06
Document6, Document2	Similarity: 0.07
Document6, Document1	Similarity: 0.04
Document6, Document18	Similarity: 0.05
Document6, Document19	Similarity: 0.05
Document6, Document16	Similarity: 0.09
Document6, Document17	Similarity: 0.06
Document5, Document4	Similarity: 0.03
Document5, Document3	Similarity: 0.09
Document5, Document2	Similarity: 0.08
Document5, Document1	Similarity: 0.02
Document5, Document18	Similarity: 0.04
Document5, Document19	Similarity: 0.05
Document5, Document16	Similarity: 0.09
Document5, Document17	Similarity: 0.10
Document4, Document3	Similarity: 0.05
Document4, Document2	Similarity: 0.06
Document4, Document1	Similarity: 0.04
Document4, Document18	Similarity: 0.08
Document4, Document19	Similarity: 0.06
Document4, Document16	Similarity: 0.04
Document4, Document17	Similarity: 0.04
Document3, Document2	Similarity: 0.05
Document3, Document1	Similarity: 0.03
Document3, Document18	Similarity: 0.11
Document3, Document19	Similarity: 0.04
Document3, Document16	Similarity: 0.06
Document3, Document17	Similarity: 0.06
Document2, Document1	Similarity: 0.03
Document2, Document18	Similarity: 0.05
Document2, Document19	Similarity: 0.04
Document2, Document16	Similarity: 0.17
Document2, Document17	Similarity: 0.10
Document1, Document18	Similarity: 0.03
Document1, Document19	Similarity: 0.02
Document1, Document16	Similarity: 0.05
Document1, Document17	Similarity: 0.02
Document18, Document19	Similarity: 0.04
Document18, Document16	Similarity: 0.03
Document18, Document17	Similarity: 0.03
Document19, Document16	Similarity: 0.07
Document19, Document17	Similarity: 0.03
Document16, Document17	Similarity: 0.10


```
**Input from large_dataset.txt**
```
Document1 Quantum computing represents a revolutionary paradigm shift from classical computing by leveraging quantum mechanical phenomena such as superposition entanglement and quantum interference to process information in fundamentally different ways. Unlike classical bits that exist in definite states of zero or one quantum bits or qubits can exist in superposition states representing both zero and one simultaneously until measured. This property enables quantum computers to explore multiple computational paths in parallel potentially solving certain complex problems exponentially faster than classical computers including cryptography optimization machine learning and scientific simulation applications.
Document2 Renewable energy technologies including solar photovoltaic wind power hydroelectric geothermal and biomass systems provide sustainable alternatives to fossil fuel consumption while reducing greenhouse gas emissions and environmental degradation. Solar panels convert sunlight directly into electricity through photovoltaic cells while wind turbines harness kinetic energy from moving air masses to generate power. Energy storage systems including lithium-ion batteries pumped hydro storage and emerging technologies like hydrogen fuel cells address intermittency challenges enabling grid stability and reliable power delivery from renewable sources across diverse geographic and climatic conditions.
Document3 Biotechnology and genetic engineering techniques manipulate biological systems and organisms to develop new products processes and applications for medicine agriculture environmental remediation and industrial manufacturing. CRISPR-Cas9 gene editing technology allows precise modification of DNA sequences enabling potential treatments for genetic diseases improved crop yields enhanced nutritional content and biofuel production. Synthetic biology combines engineering principles with biological design to create artificial biological systems and organisms with novel functions for pharmaceutical production environmental cleanup and sustainable manufacturing processes.
Document4 Space exploration and aerospace engineering advance human understanding of the universe while developing technologies for satellite communications navigation weather monitoring and planetary exploration. Rockets spacecraft and robotic probes enable scientific missions to study celestial bodies atmospheric conditions and cosmic phenomena providing insights into planetary formation stellar evolution and the potential for extraterrestrial life. Commercial space companies private partnerships and international collaborations expand access to space through reusable launch vehicles satellite constellations and planned missions to Mars and beyond.
Document5 Environmental sustainability practices focus on conservation renewable resources waste reduction and ecosystem preservation to maintain ecological balance for future generations. Circular economy principles emphasize reuse recycling and regenerative design to minimize resource consumption and environmental impact across manufacturing distribution and disposal processes. Climate change mitigation strategies include carbon sequestration renewable energy adoption sustainable transportation systems and policy frameworks promoting environmental stewardship and responsible resource management at local national and global scales.
Document6 Financial technology fintech innovations transform banking payments lending investment management and insurance services through digital platforms mobile applications and automated systems. Blockchain cryptocurrency decentralized finance and digital wallets provide alternative financial infrastructure enabling peer-to-peer transactions cross-border payments and programmable money without traditional intermediaries. Artificial intelligence machine learning and data analytics enhance risk assessment fraud detection algorithmic trading and personalized financial services while regulatory frameworks evolve to address security privacy and consumer protection concerns.
Document7 Educational technology e-learning platforms and digital learning environments expand access to knowledge and skills development through online courses virtual classrooms and interactive educational content. Personalized learning adaptive assessment systems and artificial intelligence tutoring provide customized educational experiences tailored to individual learning styles preferences and progress rates. Virtual reality augmented reality and immersive simulations create engaging educational experiences for complex subjects including science medicine engineering and history while addressing accessibility challenges and geographic barriers to quality education.
Document8 Healthcare informatics electronic health records telemedicine and medical devices integrate technology with patient care to improve diagnosis treatment outcomes and healthcare delivery efficiency. Wearable sensors remote monitoring systems and mobile health applications enable continuous health tracking preventive care and early intervention for chronic conditions. Artificial intelligence diagnostic imaging precision medicine and genomic analysis enhance clinical decision-making drug discovery and personalized treatment protocols while addressing privacy security and ethical considerations in healthcare data management.
Document9 Urban planning smart cities and sustainable infrastructure development address population growth environmental challenges and quality of life improvements in metropolitan areas. Intelligent transportation systems traffic management renewable energy grids and IoT sensors optimize resource utilization reduce congestion and enhance public services. Green building design sustainable architecture and urban agriculture promote environmental sustainability while addressing housing affordability social equity and community resilience in rapidly growing urban populations worldwide.
Document10 Manufacturing automation robotics and Industry 4.0 technologies transform production processes through cyber-physical systems digital twins and intelligent manufacturing networks. Advanced materials nanotechnology and additive manufacturing including 3D printing enable customized production lightweight structures and novel material properties for aerospace automotive electronics and medical applications. Supply chain optimization predictive maintenance and quality control systems enhance efficiency reduce costs and improve product reliability while addressing sustainability environmental impact and worker safety considerations.
Document11 Telecommunications networks 5G wireless technology and fiber optic infrastructure enable high-speed data transmission global connectivity and emerging applications including autonomous vehicles smart devices and IoT ecosystems. Network security protocols encryption standards and cybersecurity measures protect digital communications against unauthorized access data breaches and cyber attacks. Software-defined networking cloud computing and edge computing architectures provide scalable flexible infrastructure supporting diverse applications from social media to scientific research and business operations.
Document12 Agricultural technology precision farming and sustainable food production systems address global food security challenges while minimizing environmental impact and resource consumption. GPS-guided tractors drone monitoring soil sensors and automated irrigation systems optimize crop yields reduce chemical inputs and conserve water resources. Vertical farming hydroponics and controlled environment agriculture enable food production in urban areas with limited land while addressing climate change impacts on traditional farming practices.
Document13 Transportation systems autonomous vehicles electric mobility and sustainable logistics networks transform how people and goods move while addressing environmental concerns and urban congestion. Electric vehicle charging infrastructure battery technology and renewable energy integration support the transition from fossil fuel dependence toward cleaner transportation alternatives. Autonomous driving systems artificial intelligence and sensor technologies promise improved safety reduced traffic accidents and enhanced mobility access for elderly and disabled populations.
Document14 Materials science nanotechnology and advanced manufacturing techniques develop new materials with enhanced properties for applications in electronics energy storage medical devices and structural engineering. Carbon nanotubes graphene metamaterials and smart materials exhibit unique mechanical electrical and optical properties enabling innovations in computing renewable energy biomedical implants and aerospace applications. Research in materials characterization computational modeling and synthesis methods accelerates discovery and development of next-generation materials.
Document15 Cognitive science neuroscience and brain-computer interfaces explore the mechanisms of human cognition memory learning and consciousness while developing technologies to enhance human capabilities and treat neurological conditions. Neural prosthetics brain stimulation techniques and neurofeedback systems offer therapeutic applications for paralysis depression epilepsy and other neurological disorders. Research in artificial neural networks deep learning and cognitive architectures advances both understanding of biological intelligence and development of artificial intelligence systems.
Document16 Energy storage systems battery technologies and power grid modernization address renewable energy integration reliability and efficiency challenges in electrical distribution networks. Advanced battery chemistries including solid-state batteries flow batteries and supercapacitors provide improved energy density safety and longevity for applications from mobile devices to grid-scale storage. Smart grid technologies demand response systems and energy management platforms optimize electricity distribution reduce waste and accommodate distributed renewable energy sources.
Document17 Water management systems desalination technologies and environmental remediation address water scarcity pollution and ecosystem degradation challenges affecting global populations and environmental health. Advanced filtration reverse osmosis and atmospheric water generation provide clean drinking water in water-stressed regions while wastewater treatment systems protect environmental quality. Hydroponic systems water recycling and conservation practices promote sustainable water use in agriculture industry and urban development.
Document18 Pharmaceutical research drug discovery and personalized medicine advance healthcare through targeted therapies precision treatments and improved clinical outcomes for patients with diverse medical conditions. Computational drug design biomarker identification and clinical trial optimization accelerate development of safe effective medications while reducing costs and time-to-market. Regenerative medicine stem cell therapy and tissue engineering offer potential treatments for previously incurable conditions while addressing ethical considerations and regulatory requirements.
Document19 Disaster preparedness emergency response systems and resilience planning protect communities from natural disasters climate change impacts and human-caused emergencies through early warning systems evacuation planning and recovery coordination. Remote sensing satellites weather monitoring and predictive modeling enable accurate forecasting and risk assessment for hurricanes earthquakes floods and other hazardous events. Communication networks backup power systems and community preparedness programs ensure continued operation of critical infrastructure during emergencies.
Document20 Food science nutrition and sustainable agriculture practices address global nutrition challenges while promoting environmental sustainability and food system resilience. Plant-based proteins alternative meat products and nutritional enhancement techniques provide healthy sustainable food options while reducing environmental impact of traditional livestock production. Food safety systems traceability technologies and quality control measures ensure safe nutritious food supply chains from farm to consumer while addressing food waste and distribution challenges.
Document21 Artificial intelligence and machine learning have revolutionized modern computing by enabling systems to learn from data patterns without explicit programming for every scenario. Deep learning neural networks with multiple hidden layers show remarkable success in image recognition natural language processing and predictive analytics across healthcare finance and autonomous transportation industries.
Document22 Cloud computing platforms provide scalable infrastructure allowing organizations to store process and analyze massive datasets without expensive hardware investments. Amazon Web Services Microsoft Azure and Google Cloud Platform offer comprehensive solutions including virtual machines databases analytics tools and artificial intelligence services with elastic scaling capabilities.
Document23 Big data analytics examines large complex datasets to uncover hidden patterns correlations and insights for business decisions and strategic planning. Traditional database systems inadequately handle volume velocity and variety of modern data streams requiring distributed frameworks like Apache Hadoop and Apache Spark for processing petabytes across commodity hardware clusters.
Document24 Cybersecurity threats evolve with increasing digitization requiring sophisticated defense against phishing ransomware social engineering and advanced persistent threats. Organizations implement multi-factor authentication encryption intrusion detection regular audits and employee training to protect systems and maintain data integrity against malicious actors.
Document25 Internet of Things networks interconnect devices collecting exchanging and acting upon data to create smart environments improving efficiency in applications. Smart home devices industrial sensors wearable technology and connected vehicles generate continuous data streams for performance optimization predictive maintenance and enhanced user experiences through edge computing.
Document26 Blockchain technology provides decentralized immutable ledger systems enabling secure transparent transactions without intermediary institutions. Originally developed for cryptocurrency like Bitcoin blockchain applications extend to supply chain management digital identity verification smart contracts and voting systems with distributed networks resistant to tampering and single points of failure.
Document27 Software development methodologies including Agile Scrum DevOps and continuous integration practices streamline application creation deployment and maintenance processes. Modern development emphasizes iterative design user feedback automated testing version control and collaborative workflows to deliver high-quality software products efficiently and reliably.
Document28 Database management systems organize store and retrieve structured unstructured data efficiently supporting business operations analytics and decision making. Relational databases NoSQL systems distributed architectures and in-memory computing technologies handle diverse data requirements from transactional processing to real-time analytics and reporting.
Document29 Network security protocols encryption standards and authentication mechanisms protect digital communications and data transfers across public and private networks. Virtual private networks firewalls intrusion prevention systems and security monitoring tools defend against unauthorized access data breaches and cyber attacks in increasingly connected environments.
Document30 Mobile application development targets smartphones tablets and wearable devices creating user-friendly interfaces and functionalities for diverse audiences. Cross-platform frameworks native development approaches and responsive design principles ensure optimal performance user experience and accessibility across different operating systems and device specifications.
Document31 Data visualization techniques transform complex datasets into interactive charts graphs dashboards and reports enabling stakeholders to understand trends patterns and insights quickly. Business intelligence tools statistical software and visualization libraries help analysts communicate findings effectively to decision makers through compelling visual narratives.
Document32 Quality assurance testing methodologies validate software functionality performance security and usability before deployment to production environments. Automated testing manual verification regression testing and user acceptance procedures ensure applications meet requirements perform reliably and provide satisfactory user experiences across different scenarios.
Document33 Project management frameworks coordinate resources timelines budgets and deliverables to achieve organizational objectives efficiently. Traditional waterfall approaches agile methodologies and hybrid models provide structured approaches for planning executing monitoring and controlling complex projects with multiple stakeholders and dependencies.
Document34 Information systems integrate technology processes and people to collect filter process create and distribute data supporting organizational operations and strategic initiatives. Enterprise resource planning customer relationship management and business process management systems streamline workflows improve efficiency and enhance competitive advantage.
Document35 Computer graphics rendering algorithms create realistic visual effects animations and simulations for entertainment scientific visualization and engineering applications. GPU acceleration ray tracing and real-time rendering techniques produce high-quality images and interactive experiences in gaming movies virtual reality and augmented reality environments.
Document36 Artificial intelligence and machine learning have revolutionized modern computing by enabling systems to learn from data patterns without explicit programming for every scenario. Deep learning neural networks with multiple hidden layers show remarkable success in image recognition natural language processing and predictive analytics across healthcare finance and autonomous transportation industries.
Document37 Cloud computing platforms provide scalable infrastructure allowing organizations to store process and analyze massive datasets without expensive hardware investments. Amazon Web Services Microsoft Azure and Google Cloud Platform offer comprehensive solutions including virtual machines databases analytics tools and artificial intelligence services with elastic scaling capabilities.
Document38 Big data analytics examines large complex datasets to uncover hidden patterns correlations and insights for business decisions and strategic planning. Traditional database systems inadequately handle volume velocity and variety of modern data streams requiring distributed frameworks like Apache Hadoop and Apache Spark for processing petabytes across commodity hardware clusters.
Document39 Cybersecurity threats evolve with increasing digitization requiring sophisticated defense against phishing ransomware social engineering and advanced persistent threats. Organizations implement multi-factor authentication encryption intrusion detection regular audits and employee training to protect systems and maintain data integrity against malicious actors.
Document40 Internet of Things networks interconnect devices collecting exchanging and acting upon data to create smart environments improving efficiency in applications. Smart home devices industrial sensors wearable technology and connected vehicles generate continuous data streams for performance optimization predictive maintenance and enhanced user experiences through edge computing.
Document41 Blockchain technology provides decentralized immutable ledger systems enabling secure transparent transactions without intermediary institutions. Originally developed for cryptocurrency like Bitcoin blockchain applications extend to supply chain management digital identity verification smart contracts and voting systems with distributed networks resistant to tampering and single points of failure.
Document42 Software development methodologies including Agile Scrum DevOps and continuous integration practices streamline application creation deployment and maintenance processes. Modern development emphasizes iterative design user feedback automated testing version control and collaborative workflows to deliver high-quality software products efficiently and reliably.
Document43 Database management systems organize store and retrieve structured unstructured data efficiently supporting business operations analytics and decision making. Relational databases NoSQL systems distributed architectures and in-memory computing technologies handle diverse data requirements from transactional processing to real-time analytics and reporting.
Document44 Network security protocols encryption standards and authentication mechanisms protect digital communications and data transfers across public and private networks. Virtual private networks firewalls intrusion prevention systems and security monitoring tools defend against unauthorized access data breaches and cyber attacks in increasingly connected environments.
Document45 Mobile application development targets smartphones tablets and wearable devices creating user-friendly interfaces and functionalities for diverse audiences. Cross-platform frameworks native development approaches and responsive design principles ensure optimal performance user experience and accessibility across different operating systems and device specifications.
Document46 Data visualization techniques transform complex datasets into interactive charts graphs dashboards and reports enabling stakeholders to understand trends patterns and insights quickly. Business intelligence tools statistical software and visualization libraries help analysts communicate findings effectively to decision makers through compelling visual narratives.
Document47 Quality assurance testing methodologies validate software functionality performance security and usability before deployment to production environments. Automated testing manual verification regression testing and user acceptance procedures ensure applications meet requirements perform reliably and provide satisfactory user experiences across different scenarios.
Document48 Project management frameworks coordinate resources timelines budgets and deliverables to achieve organizational objectives efficiently. Traditional waterfall approaches agile methodologies and hybrid models provide structured approaches for planning executing monitoring and controlling complex projects with multiple stakeholders and dependencies.
Document49 Information systems integrate technology processes and people to collect filter process create and distribute data supporting organizational operations and strategic initiatives. Enterprise resource planning customer relationship management and business process management systems streamline workflows improve efficiency and enhance competitive advantage.
Document50 Computer graphics rendering algorithms create realistic visual effects animations and simulations for entertainment scientific visualization and engineering applications. GPU acceleration ray tracing and real-time rendering techniques produce high-quality images and interactive experiences in gaming movies virtual reality and augmented reality environments.
```


**Output from large_dataset.txt**
```
Document25, Document26	Similarity: 0.11
Document25, Document23	Similarity: 0.08
Document25, Document24	Similarity: 0.04
Document25, Document21	Similarity: 0.10
Document25, Document22	Similarity: 0.04
Document25, Document20	Similarity: 0.03
Document25, Document18	Similarity: 0.06
Document25, Document19	Similarity: 0.07
Document25, Document16	Similarity: 0.11
Document25, Document17	Similarity: 0.02
Document25, Document14	Similarity: 0.11
Document25, Document15	Similarity: 0.08
Document25, Document12	Similarity: 0.04
Document25, Document13	Similarity: 0.07
Document25, Document10	Similarity: 0.10
Document25, Document11	Similarity: 0.12
Document25, Document50	Similarity: 0.10
Document25, Document49	Similarity: 0.09
Document25, Document47	Similarity: 0.10
Document25, Document48	Similarity: 0.04
Document25, Document45	Similarity: 0.09
Document25, Document46	Similarity: 0.05
Document25, Document43	Similarity: 0.06
Document25, Document44	Similarity: 0.09
Document25, Document41	Similarity: 0.11
Document25, Document42	Similarity: 0.07
Document25, Document40	Similarity: 1.00
Document25, Document38	Similarity: 0.08
Document25, Document39	Similarity: 0.04
Document25, Document36	Similarity: 0.10
Document25, Document37	Similarity: 0.04
Document25, Document34	Similarity: 0.09
Document25, Document35	Similarity: 0.10
Document25, Document32	Similarity: 0.10
Document25, Document33	Similarity: 0.04
Document25, Document30	Similarity: 0.09
Document25, Document31	Similarity: 0.05
Document25, Document9	Similarity: 0.05
Document25, Document8	Similarity: 0.13
Document25, Document7	Similarity: 0.09
Document25, Document6	Similarity: 0.06
Document25, Document5	Similarity: 0.03
Document25, Document4	Similarity: 0.06
Document25, Document3	Similarity: 0.10
Document25, Document2	Similarity: 0.04
Document25, Document1	Similarity: 0.07
Document25, Document29	Similarity: 0.09
Document25, Document27	Similarity: 0.07
Document25, Document28	Similarity: 0.06
Document26, Document23	Similarity: 0.09
Document26, Document24	Similarity: 0.05
Document26, Document21	Similarity: 0.10
Document26, Document22	Similarity: 0.05
Document26, Document20	Similarity: 0.06
Document26, Document18	Similarity: 0.04
Document26, Document19	Similarity: 0.05
Document26, Document16	Similarity: 0.11
Document26, Document17	Similarity: 0.04
Document26, Document14	Similarity: 0.08
Document26, Document15	Similarity: 0.08
Document26, Document12	Similarity: 0.04
Document26, Document13	Similarity: 0.05
Document26, Document10	Similarity: 0.09
Document26, Document11	Similarity: 0.07
Document26, Document50	Similarity: 0.04
Document26, Document49	Similarity: 0.07
Document26, Document47	Similarity: 0.05
Document26, Document48	Similarity: 0.07
Document26, Document45	Similarity: 0.04
Document26, Document46	Similarity: 0.04
Document26, Document43	Similarity: 0.07
Document26, Document44	Similarity: 0.05
Document26, Document41	Similarity: 1.00
Document26, Document42	Similarity: 0.03
Document26, Document40	Similarity: 0.11
Document26, Document38	Similarity: 0.09
Document26, Document39	Similarity: 0.05
Document26, Document36	Similarity: 0.10
Document26, Document37	Similarity: 0.05
Document26, Document34	Similarity: 0.07
Document26, Document35	Similarity: 0.04
Document26, Document32	Similarity: 0.05
Document26, Document33	Similarity: 0.07
Document26, Document30	Similarity: 0.04
Document26, Document31	Similarity: 0.04
Document26, Document9	Similarity: 0.05
Document26, Document8	Similarity: 0.08
Document26, Document7	Similarity: 0.06
Document26, Document6	Similarity: 0.14
Document26, Document5	Similarity: 0.05
Document26, Document4	Similarity: 0.04
Document26, Document3	Similarity: 0.10
Document26, Document2	Similarity: 0.05
Document26, Document1	Similarity: 0.04
Document26, Document29	Similarity: 0.05
Document26, Document27	Similarity: 0.03
Document26, Document28	Similarity: 0.07
Document23, Document24	Similarity: 0.07
Document23, Document21	Similarity: 0.14
Document23, Document22	Similarity: 0.06
Document23, Document20	Similarity: 0.06
Document23, Document18	Similarity: 0.03
Document23, Document19	Similarity: 0.05
Document23, Document16	Similarity: 0.06
Document23, Document17	Similarity: 0.02
Document23, Document14	Similarity: 0.03
Document23, Document15	Similarity: 0.06
Document23, Document12	Similarity: 0.03
Document23, Document13	Similarity: 0.03
Document23, Document10	Similarity: 0.03
Document23, Document11	Similarity: 0.04
Document23, Document50	Similarity: 0.03
Document23, Document49	Similarity: 0.10
Document23, Document47	Similarity: 0.04
Document23, Document48	Similarity: 0.10
Document23, Document45	Similarity: 0.07
Document23, Document46	Similarity: 0.11
Document23, Document43	Similarity: 0.15
Document23, Document44	Similarity: 0.05
Document23, Document41	Similarity: 0.09
Document23, Document42	Similarity: 0.04
Document23, Document40	Similarity: 0.08
Document23, Document38	Similarity: 1.00
Document23, Document39	Similarity: 0.07
Document23, Document36	Similarity: 0.14
Document23, Document37	Similarity: 0.06
Document23, Document34	Similarity: 0.10
Document23, Document35	Similarity: 0.03
Document23, Document32	Similarity: 0.04
Document23, Document33	Similarity: 0.10
Document23, Document30	Similarity: 0.07
Document23, Document31	Similarity: 0.11
Document23, Document9	Similarity: 0.04
Document23, Document8	Similarity: 0.05
Document23, Document7	Similarity: 0.05
Document23, Document6	Similarity: 0.07
Document23, Document5	Similarity: 0.06
Document23, Document4	Similarity: 0.05
Document23, Document3	Similarity: 0.05
Document23, Document2	Similarity: 0.05
Document23, Document1	Similarity: 0.04
Document23, Document29	Similarity: 0.05
Document23, Document27	Similarity: 0.04
Document23, Document28	Similarity: 0.15
Document24, Document21	Similarity: 0.06
Document24, Document22	Similarity: 0.05
Document24, Document20	Similarity: 0.04
Document24, Document18	Similarity: 0.03
Document24, Document19	Similarity: 0.03
Document24, Document16	Similarity: 0.05
Document24, Document17	Similarity: 0.05
Document24, Document14	Similarity: 0.05
Document24, Document15	Similarity: 0.04
Document24, Document12	Similarity: 0.03
Document24, Document13	Similarity: 0.02
Document24, Document10	Similarity: 0.03
Document24, Document11	Similarity: 0.09
Document24, Document50	Similarity: 0.03
Document24, Document49	Similarity: 0.06
Document24, Document47	Similarity: 0.03
Document24, Document48	Similarity: 0.04
Document24, Document45	Similarity: 0.03
Document24, Document46	Similarity: 0.04
Document24, Document43	Similarity: 0.06
Document24, Document44	Similarity: 0.13
Document24, Document41	Similarity: 0.05
Document24, Document42	Similarity: 0.03
Document24, Document40	Similarity: 0.04
Document24, Document38	Similarity: 0.07
Document24, Document39	Similarity: 1.00
Document24, Document36	Similarity: 0.06
Document24, Document37	Similarity: 0.05
Document24, Document34	Similarity: 0.06
Document24, Document35	Similarity: 0.03
Document24, Document32	Similarity: 0.03
Document24, Document33	Similarity: 0.04
Document24, Document30	Similarity: 0.03
Document24, Document31	Similarity: 0.04
Document24, Document9	Similarity: 0.03
Document24, Document8	Similarity: 0.05
Document24, Document7	Similarity: 0.04
Document24, Document6	Similarity: 0.07
Document24, Document5	Similarity: 0.04
Document24, Document4	Similarity: 0.03
Document24, Document3	Similarity: 0.06
Document24, Document2	Similarity: 0.03
Document24, Document1	Similarity: 0.02
Document24, Document29	Similarity: 0.13
Document24, Document27	Similarity: 0.03
Document24, Document28	Similarity: 0.06
Document21, Document22	Similarity: 0.10
Document21, Document20	Similarity: 0.04
Document21, Document18	Similarity: 0.04
Document21, Document19	Similarity: 0.07
Document21, Document16	Similarity: 0.08
Document21, Document17	Similarity: 0.03
Document21, Document14	Similarity: 0.07
Document21, Document15	Similarity: 0.12
Document21, Document12	Similarity: 0.04
Document21, Document13	Similarity: 0.10
Document21, Document10	Similarity: 0.05
Document21, Document11	Similarity: 0.07
Document21, Document50	Similarity: 0.04
Document21, Document49	Similarity: 0.05
Document21, Document47	Similarity: 0.04
Document21, Document48	Similarity: 0.07
Document21, Document45	Similarity: 0.05
Document21, Document46	Similarity: 0.08
Document21, Document43	Similarity: 0.11
Document21, Document44	Similarity: 0.08
Document21, Document41	Similarity: 0.10
Document21, Document42	Similarity: 0.04
Document21, Document40	Similarity: 0.10
Document21, Document38	Similarity: 0.14
Document21, Document39	Similarity: 0.06
Document21, Document36	Similarity: 1.00
Document21, Document37	Similarity: 0.10
Document21, Document34	Similarity: 0.05
Document21, Document35	Similarity: 0.04
Document21, Document32	Similarity: 0.04
Document21, Document33	Similarity: 0.07
Document21, Document30	Similarity: 0.05
Document21, Document31	Similarity: 0.08
Document21, Document9	Similarity: 0.04
Document21, Document8	Similarity: 0.10
Document21, Document7	Similarity: 0.07
Document21, Document6	Similarity: 0.12
Document21, Document5	Similarity: 0.06
Document21, Document4	Similarity: 0.03
Document21, Document3	Similarity: 0.07
Document21, Document2	Similarity: 0.06
Document21, Document1	Similarity: 0.08
Document21, Document29	Similarity: 0.08
Document21, Document27	Similarity: 0.04
Document21, Document28	Similarity: 0.11
Document22, Document20	Similarity: 0.03
Document22, Document18	Similarity: 0.03
Document22, Document19	Similarity: 0.02
Document22, Document16	Similarity: 0.06
Document22, Document17	Similarity: 0.02
Document22, Document14	Similarity: 0.03
Document22, Document15	Similarity: 0.07
Document22, Document12	Similarity: 0.02
Document22, Document13	Similarity: 0.04
Document22, Document10	Similarity: 0.02
Document22, Document11	Similarity: 0.09
Document22, Document50	Similarity: 0.03
Document22, Document49	Similarity: 0.04
Document22, Document47	Similarity: 0.04
Document22, Document48	Similarity: 0.06
Document22, Document45	Similarity: 0.01
Document22, Document46	Similarity: 0.07
Document22, Document43	Similarity: 0.09
Document22, Document44	Similarity: 0.04
Document22, Document41	Similarity: 0.05
Document22, Document42	Similarity: 0.04
Document22, Document40	Similarity: 0.04
Document22, Document38	Similarity: 0.06
Document22, Document39	Similarity: 0.05
Document22, Document36	Similarity: 0.10
Document22, Document37	Similarity: 1.00
Document22, Document34	Similarity: 0.04
Document22, Document35	Similarity: 0.03
Document22, Document32	Similarity: 0.04
Document22, Document33	Similarity: 0.06
Document22, Document30	Similarity: 0.01
Document22, Document31	Similarity: 0.07
Document22, Document9	Similarity: 0.03
Document22, Document8	Similarity: 0.05
Document22, Document7	Similarity: 0.09
Document22, Document6	Similarity: 0.11
Document22, Document5	Similarity: 0.02
Document22, Document4	Similarity: 0.02
Document22, Document3	Similarity: 0.04
Document22, Document2	Similarity: 0.04
Document22, Document1	Similarity: 0.05
Document22, Document29	Similarity: 0.04
Document22, Document27	Similarity: 0.04
Document22, Document28	Similarity: 0.09
Document20, Document18	Similarity: 0.06
Document20, Document19	Similarity: 0.06
Document20, Document16	Similarity: 0.12
Document20, Document17	Similarity: 0.15
Document20, Document14	Similarity: 0.04
Document20, Document15	Similarity: 0.08
Document20, Document12	Similarity: 0.16
Document20, Document13	Similarity: 0.09
Document20, Document10	Similarity: 0.13
Document20, Document11	Similarity: 0.06
Document20, Document50	Similarity: 0.02
Document20, Document49	Similarity: 0.04
Document20, Document47	Similarity: 0.07
Document20, Document48	Similarity: 0.05
Document20, Document45	Similarity: 0.04
Document20, Document46	Similarity: 0.03
Document20, Document43	Similarity: 0.06
Document20, Document44	Similarity: 0.02
Document20, Document41	Similarity: 0.06
Document20, Document42	Similarity: 0.06
Document20, Document40	Similarity: 0.03
Document20, Document38	Similarity: 0.06
Document20, Document39	Similarity: 0.04
Document20, Document36	Similarity: 0.04
Document20, Document37	Similarity: 0.03
Document20, Document34	Similarity: 0.04
Document20, Document35	Similarity: 0.02
Document20, Document32	Similarity: 0.07
Document20, Document33	Similarity: 0.05
Document20, Document30	Similarity: 0.04
Document20, Document31	Similarity: 0.03
Document20, Document9	Similarity: 0.14
Document20, Document8	Similarity: 0.05
Document20, Document7	Similarity: 0.09
Document20, Document6	Similarity: 0.09
Document20, Document5	Similarity: 0.12
Document20, Document4	Similarity: 0.05
Document20, Document3	Similarity: 0.11
Document20, Document2	Similarity: 0.11
Document20, Document1	Similarity: 0.03
Document20, Document29	Similarity: 0.02
Document20, Document27	Similarity: 0.06
Document20, Document28	Similarity: 0.06
Document18, Document19	Similarity: 0.04
Document18, Document16	Similarity: 0.03
Document18, Document17	Similarity: 0.03
Document18, Document14	Similarity: 0.11
Document18, Document15	Similarity: 0.08
Document18, Document12	Similarity: 0.05
Document18, Document13	Similarity: 0.05
Document18, Document10	Similarity: 0.09
Document18, Document11	Similarity: 0.03
Document18, Document50	Similarity: 0.03
Document18, Document49	Similarity: 0.01
Document18, Document47	Similarity: 0.02
Document18, Document48	Similarity: 0.04
Document18, Document45	Similarity: 0.06
Document18, Document46	Similarity: 0.02
Document18, Document43	Similarity: 0.04
Document18, Document44	Similarity: 0.01
Document18, Document41	Similarity: 0.04
Document18, Document42	Similarity: 0.03
Document18, Document40	Similarity: 0.06
Document18, Document38	Similarity: 0.03
Document18, Document39	Similarity: 0.03
Document18, Document36	Similarity: 0.04
Document18, Document37	Similarity: 0.03
Document18, Document34	Similarity: 0.01
Document18, Document35	Similarity: 0.03
Document18, Document32	Similarity: 0.02
Document18, Document33	Similarity: 0.04
Document18, Document30	Similarity: 0.06
Document18, Document31	Similarity: 0.02
Document18, Document9	Similarity: 0.06
Document18, Document8	Similarity: 0.17
Document18, Document7	Similarity: 0.09
Document18, Document6	Similarity: 0.05
Document18, Document5	Similarity: 0.04
Document18, Document4	Similarity: 0.08
Document18, Document3	Similarity: 0.11
Document18, Document2	Similarity: 0.05
Document18, Document1	Similarity: 0.03
Document18, Document29	Similarity: 0.01
Document18, Document27	Similarity: 0.03
Document18, Document28	Similarity: 0.04
Document19, Document16	Similarity: 0.07
Document19, Document17	Similarity: 0.03
Document19, Document14	Similarity: 0.04
Document19, Document15	Similarity: 0.06
Document19, Document12	Similarity: 0.07
Document19, Document13	Similarity: 0.06
Document19, Document10	Similarity: 0.06
Document19, Document11	Similarity: 0.06
Document19, Document50	Similarity: 0.02
Document19, Document49	Similarity: 0.03
Document19, Document47	Similarity: 0.02
Document19, Document48	Similarity: 0.05
Document19, Document45	Similarity: 0.05
Document19, Document46	Similarity: 0.02
Document19, Document43	Similarity: 0.03
Document19, Document44	Similarity: 0.06
Document19, Document41	Similarity: 0.05
Document19, Document42	Similarity: 0.01
Document19, Document40	Similarity: 0.07
Document19, Document38	Similarity: 0.05
Document19, Document39	Similarity: 0.03
Document19, Document36	Similarity: 0.07
Document19, Document37	Similarity: 0.02
Document19, Document34	Similarity: 0.03
Document19, Document35	Similarity: 0.02
Document19, Document32	Similarity: 0.02
Document19, Document33	Similarity: 0.05
Document19, Document30	Similarity: 0.05
Document19, Document31	Similarity: 0.02
Document19, Document9	Similarity: 0.07
Document19, Document8	Similarity: 0.06
Document19, Document7	Similarity: 0.05
Document19, Document6	Similarity: 0.05
Document19, Document5	Similarity: 0.05
Document19, Document4	Similarity: 0.06
Document19, Document3	Similarity: 0.04
Document19, Document2	Similarity: 0.04
Document19, Document1	Similarity: 0.02
Document19, Document29	Similarity: 0.06
Document19, Document27	Similarity: 0.01
Document19, Document28	Similarity: 0.03
Document16, Document17	Similarity: 0.10
Document16, Document14	Similarity: 0.12
Document16, Document15	Similarity: 0.09
Document16, Document12	Similarity: 0.07
Document16, Document13	Similarity: 0.13
Document16, Document10	Similarity: 0.12
Document16, Document11	Similarity: 0.09
Document16, Document50	Similarity: 0.05
Document16, Document49	Similarity: 0.06
Document16, Document47	Similarity: 0.05
Document16, Document48	Similarity: 0.06
Document16, Document45	Similarity: 0.06
Document16, Document46	Similarity: 0.02
Document16, Document43	Similarity: 0.09
Document16, Document44	Similarity: 0.05
Document16, Document41	Similarity: 0.11
Document16, Document42	Similarity: 0.05
Document16, Document40	Similarity: 0.11
Document16, Document38	Similarity: 0.06
Document16, Document39	Similarity: 0.05
Document16, Document36	Similarity: 0.08
Document16, Document37	Similarity: 0.06
Document16, Document34	Similarity: 0.06
Document16, Document35	Similarity: 0.05
Document16, Document32	Similarity: 0.05
Document16, Document33	Similarity: 0.06
Document16, Document30	Similarity: 0.06
Document16, Document31	Similarity: 0.02
Document16, Document9	Similarity: 0.11
Document16, Document8	Similarity: 0.10
Document16, Document7	Similarity: 0.08
Document16, Document6	Similarity: 0.09
Document16, Document5	Similarity: 0.09
Document16, Document4	Similarity: 0.04
Document16, Document3	Similarity: 0.06
Document16, Document2	Similarity: 0.17
Document16, Document1	Similarity: 0.05
Document16, Document29	Similarity: 0.05
Document16, Document27	Similarity: 0.05
Document16, Document28	Similarity: 0.09
Document17, Document14	Similarity: 0.04
Document17, Document15	Similarity: 0.07
Document17, Document12	Similarity: 0.15
Document17, Document13	Similarity: 0.09
Document17, Document10	Similarity: 0.08
Document17, Document11	Similarity: 0.04
Document17, Document50	Similarity: 0.03
Document17, Document49	Similarity: 0.04
Document17, Document47	Similarity: 0.04
Document17, Document48	Similarity: 0.04
Document17, Document45	Similarity: 0.04
Document17, Document46	Similarity: 0.01
Document17, Document43	Similarity: 0.05
Document17, Document44	Similarity: 0.05
Document17, Document41	Similarity: 0.04
Document17, Document42	Similarity: 0.04
Document17, Document40	Similarity: 0.02
Document17, Document38	Similarity: 0.02
Document17, Document39	Similarity: 0.05
Document17, Document36	Similarity: 0.03
Document17, Document37	Similarity: 0.02
Document17, Document34	Similarity: 0.04
Document17, Document35	Similarity: 0.03
Document17, Document32	Similarity: 0.04
Document17, Document33	Similarity: 0.04
Document17, Document30	Similarity: 0.04
Document17, Document31	Similarity: 0.01
Document17, Document9	Similarity: 0.17
Document17, Document8	Similarity: 0.07
Document17, Document7	Similarity: 0.07
Document17, Document6	Similarity: 0.06
Document17, Document5	Similarity: 0.10
Document17, Document4	Similarity: 0.04
Document17, Document3	Similarity: 0.06
Document17, Document2	Similarity: 0.10
Document17, Document1	Similarity: 0.02
Document17, Document29	Similarity: 0.05
Document17, Document27	Similarity: 0.04
Document17, Document28	Similarity: 0.05
Document14, Document15	Similarity: 0.10
Document14, Document12	Similarity: 0.03
Document14, Document13	Similarity: 0.05
Document14, Document10	Similarity: 0.11
Document14, Document11	Similarity: 0.06
Document14, Document50	Similarity: 0.08
Document14, Document49	Similarity: 0.01
Document14, Document47	Similarity: 0.02
Document14, Document48	Similarity: 0.04
Document14, Document45	Similarity: 0.05
Document14, Document46	Similarity: 0.04
Document14, Document43	Similarity: 0.02
Document14, Document44	Similarity: 0.02
Document14, Document41	Similarity: 0.08
Document14, Document42	Similarity: 0.02
Document14, Document40	Similarity: 0.11
Document14, Document38	Similarity: 0.03
Document14, Document39	Similarity: 0.05
Document14, Document36	Similarity: 0.07
Document14, Document37	Similarity: 0.03
Document14, Document34	Similarity: 0.01
Document14, Document35	Similarity: 0.08
Document14, Document32	Similarity: 0.02
Document14, Document33	Similarity: 0.04
Document14, Document30	Similarity: 0.05
Document14, Document31	Similarity: 0.04
Document14, Document9	Similarity: 0.07
Document14, Document8	Similarity: 0.08
Document14, Document7	Similarity: 0.05
Document14, Document6	Similarity: 0.04
Document14, Document5	Similarity: 0.06
Document14, Document4	Similarity: 0.05
Document14, Document3	Similarity: 0.13
Document14, Document2	Similarity: 0.05
Document14, Document1	Similarity: 0.06
Document14, Document29	Similarity: 0.02
Document14, Document27	Similarity: 0.02
Document14, Document28	Similarity: 0.02
Document15, Document12	Similarity: 0.04
Document15, Document13	Similarity: 0.09
Document15, Document10	Similarity: 0.08
Document15, Document11	Similarity: 0.06
Document15, Document50	Similarity: 0.06
Document15, Document49	Similarity: 0.05
Document15, Document47	Similarity: 0.04
Document15, Document48	Similarity: 0.04
Document15, Document45	Similarity: 0.06
Document15, Document46	Similarity: 0.05
Document15, Document43	Similarity: 0.06
Document15, Document44	Similarity: 0.06
Document15, Document41	Similarity: 0.08
Document15, Document42	Similarity: 0.04
Document15, Document40	Similarity: 0.08
Document15, Document38	Similarity: 0.06
Document15, Document39	Similarity: 0.04
Document15, Document36	Similarity: 0.12
Document15, Document37	Similarity: 0.07
Document15, Document34	Similarity: 0.05
Document15, Document35	Similarity: 0.06
Document15, Document32	Similarity: 0.04
Document15, Document33	Similarity: 0.04
Document15, Document30	Similarity: 0.06
Document15, Document31	Similarity: 0.05
Document15, Document9	Similarity: 0.07
Document15, Document8	Similarity: 0.11
Document15, Document7	Similarity: 0.10
Document15, Document6	Similarity: 0.09
Document15, Document5	Similarity: 0.04
Document15, Document4	Similarity: 0.11
Document15, Document3	Similarity: 0.09
Document15, Document2	Similarity: 0.05
Document15, Document1	Similarity: 0.07
Document15, Document29	Similarity: 0.06
Document15, Document27	Similarity: 0.04
Document15, Document28	Similarity: 0.06
Document12, Document13	Similarity: 0.08
Document12, Document10	Similarity: 0.09
Document12, Document11	Similarity: 0.05
Document12, Document50	Similarity: 0.02
Document12, Document49	Similarity: 0.05
Document12, Document47	Similarity: 0.05
Document12, Document48	Similarity: 0.06
Document12, Document45	Similarity: 0.02
Document12, Document46	Similarity: 0.01
Document12, Document43	Similarity: 0.02
Document12, Document44	Similarity: 0.06
Document12, Document41	Similarity: 0.04
Document12, Document42	Similarity: 0.03
Document12, Document40	Similarity: 0.04
Document12, Document38	Similarity: 0.03
Document12, Document39	Similarity: 0.03
Document12, Document36	Similarity: 0.04
Document12, Document37	Similarity: 0.02
Document12, Document34	Similarity: 0.05
Document12, Document35	Similarity: 0.02
Document12, Document32	Similarity: 0.05
Document12, Document33	Similarity: 0.06
Document12, Document30	Similarity: 0.02
Document12, Document31	Similarity: 0.01
Document12, Document9	Similarity: 0.17
Document12, Document8	Similarity: 0.12
Document12, Document7	Similarity: 0.06
Document12, Document6	Similarity: 0.07
Document12, Document5	Similarity: 0.13
Document12, Document4	Similarity: 0.04
Document12, Document3	Similarity: 0.10
Document12, Document2	Similarity: 0.07
Document12, Document1	Similarity: 0.02
Document12, Document29	Similarity: 0.06
Document12, Document27	Similarity: 0.03
Document12, Document28	Similarity: 0.02
Document13, Document10	Similarity: 0.10
Document13, Document11	Similarity: 0.07
Document13, Document50	Similarity: 0.02
Document13, Document49	Similarity: 0.05
Document13, Document47	Similarity: 0.01
Document13, Document48	Similarity: 0.02
Document13, Document45	Similarity: 0.03
Document13, Document46	Similarity: 0.03
Document13, Document43	Similarity: 0.05
Document13, Document44	Similarity: 0.05
Document13, Document41	Similarity: 0.05
Document13, Document42	Similarity: 0.02
Document13, Document40	Similarity: 0.07
Document13, Document38	Similarity: 0.03
Document13, Document39	Similarity: 0.02
Document13, Document36	Similarity: 0.10
Document13, Document37	Similarity: 0.04
Document13, Document34	Similarity: 0.05
Document13, Document35	Similarity: 0.02
Document13, Document32	Similarity: 0.01
Document13, Document33	Similarity: 0.02
Document13, Document30	Similarity: 0.03
Document13, Document31	Similarity: 0.03
Document13, Document9	Similarity: 0.14
Document13, Document8	Similarity: 0.07
Document13, Document7	Similarity: 0.08
Document13, Document6	Similarity: 0.08
Document13, Document5	Similarity: 0.07
Document13, Document4	Similarity: 0.06
Document13, Document3	Similarity: 0.09
Document13, Document2	Similarity: 0.11
Document13, Document1	Similarity: 0.02
Document13, Document29	Similarity: 0.05
Document13, Document27	Similarity: 0.02
Document13, Document28	Similarity: 0.05
Document10, Document11	Similarity: 0.05
Document10, Document50	Similarity: 0.03
Document10, Document49	Similarity: 0.07
Document10, Document47	Similarity: 0.04
Document10, Document48	Similarity: 0.02
Document10, Document45	Similarity: 0.03
Document10, Document46	Similarity: 0.03
Document10, Document43	Similarity: 0.03
Document10, Document44	Similarity: 0.04
Document10, Document41	Similarity: 0.09
Document10, Document42	Similarity: 0.06
Document10, Document40	Similarity: 0.10
Document10, Document38	Similarity: 0.03
Document10, Document39	Similarity: 0.03
Document10, Document36	Similarity: 0.05
Document10, Document37	Similarity: 0.02
Document10, Document34	Similarity: 0.07
Document10, Document35	Similarity: 0.03
Document10, Document32	Similarity: 0.04
Document10, Document33	Similarity: 0.02
Document10, Document30	Similarity: 0.03
Document10, Document31	Similarity: 0.03
Document10, Document9	Similarity: 0.09
Document10, Document8	Similarity: 0.11
Document10, Document7	Similarity: 0.09
Document10, Document6	Similarity: 0.07
Document10, Document5	Similarity: 0.07
Document10, Document4	Similarity: 0.06
Document10, Document3	Similarity: 0.08
Document10, Document2	Similarity: 0.06
Document10, Document1	Similarity: 0.03
Document10, Document29	Similarity: 0.04
Document10, Document27	Similarity: 0.06
Document10, Document28	Similarity: 0.03
Document11, Document50	Similarity: 0.03
Document11, Document49	Similarity: 0.08
Document11, Document47	Similarity: 0.06
Document11, Document48	Similarity: 0.03
Document11, Document45	Similarity: 0.03
Document11, Document46	Similarity: 0.04
Document11, Document43	Similarity: 0.12
Document11, Document44	Similarity: 0.22
Document11, Document41	Similarity: 0.07
Document11, Document42	Similarity: 0.03
Document11, Document40	Similarity: 0.12
Document11, Document38	Similarity: 0.04
Document11, Document39	Similarity: 0.09
Document11, Document36	Similarity: 0.07
Document11, Document37	Similarity: 0.09
Document11, Document34	Similarity: 0.08
Document11, Document35	Similarity: 0.03
Document11, Document32	Similarity: 0.06
Document11, Document33	Similarity: 0.03
Document11, Document30	Similarity: 0.03
Document11, Document31	Similarity: 0.04
Document11, Document9	Similarity: 0.05
Document11, Document8	Similarity: 0.08
Document11, Document7	Similarity: 0.06
Document11, Document6	Similarity: 0.08
Document11, Document5	Similarity: 0.03
Document11, Document4	Similarity: 0.06
Document11, Document3	Similarity: 0.04
Document11, Document2	Similarity: 0.06
Document11, Document1	Similarity: 0.06
Document11, Document29	Similarity: 0.22
Document11, Document27	Similarity: 0.03
Document11, Document28	Similarity: 0.12
Document50, Document49	Similarity: 0.03
Document50, Document47	Similarity: 0.06
Document50, Document48	Similarity: 0.03
Document50, Document45	Similarity: 0.03
Document50, Document46	Similarity: 0.07
Document50, Document43	Similarity: 0.03
Document50, Document44	Similarity: 0.06
Document50, Document41	Similarity: 0.04
Document50, Document42	Similarity: 0.03
Document50, Document40	Similarity: 0.10
Document50, Document38	Similarity: 0.03
Document50, Document39	Similarity: 0.03
Document50, Document36	Similarity: 0.04
Document50, Document37	Similarity: 0.03
Document50, Document34	Similarity: 0.03
Document50, Document35	Similarity: 1.00
Document50, Document32	Similarity: 0.06
Document50, Document33	Similarity: 0.03
Document50, Document30	Similarity: 0.03
Document50, Document31	Similarity: 0.07
Document50, Document9	Similarity: 0.02
Document50, Document8	Similarity: 0.04
Document50, Document7	Similarity: 0.13
Document50, Document6	Similarity: 0.02
Document50, Document5	Similarity: 0.02
Document50, Document4	Similarity: 0.04
Document50, Document3	Similarity: 0.07
Document50, Document2	Similarity: 0.01
Document50, Document1	Similarity: 0.04
Document50, Document29	Similarity: 0.06
Document50, Document27	Similarity: 0.03
Document50, Document28	Similarity: 0.03
Document49, Document47	Similarity: 0.03
Document49, Document48	Similarity: 0.08
Document49, Document45	Similarity: 0.03
Document49, Document46	Similarity: 0.06
Document49, Document43	Similarity: 0.14
Document49, Document44	Similarity: 0.05
Document49, Document41	Similarity: 0.07
Document49, Document42	Similarity: 0.08
Document49, Document40	Similarity: 0.09
Document49, Document38	Similarity: 0.10
Document49, Document39	Similarity: 0.06
Document49, Document36	Similarity: 0.05
Document49, Document37	Similarity: 0.04
Document49, Document34	Similarity: 1.00
Document49, Document35	Similarity: 0.03
Document49, Document32	Similarity: 0.03
Document49, Document33	Similarity: 0.08
Document49, Document30	Similarity: 0.03
Document49, Document31	Similarity: 0.06
Document49, Document9	Similarity: 0.07
Document49, Document8	Similarity: 0.12
Document49, Document7	Similarity: 0.06
Document49, Document6	Similarity: 0.08
Document49, Document5	Similarity: 0.07
Document49, Document4	Similarity: 0.02
Document49, Document3	Similarity: 0.07
Document49, Document2	Similarity: 0.03
Document49, Document1	Similarity: 0.04
Document49, Document29	Similarity: 0.05
Document49, Document27	Similarity: 0.08
Document49, Document28	Similarity: 0.14
Document47, Document48	Similarity: 0.06
Document47, Document45	Similarity: 0.09
Document47, Document46	Similarity: 0.04
Document47, Document43	Similarity: 0.05
Document47, Document44	Similarity: 0.06
Document47, Document41	Similarity: 0.05
Document47, Document42	Similarity: 0.15
Document47, Document40	Similarity: 0.10
Document47, Document38	Similarity: 0.04
Document47, Document39	Similarity: 0.03
Document47, Document36	Similarity: 0.04
Document47, Document37	Similarity: 0.04
Document47, Document34	Similarity: 0.03
Document47, Document35	Similarity: 0.06
Document47, Document32	Similarity: 1.00
Document47, Document33	Similarity: 0.06
Document47, Document30	Similarity: 0.09
Document47, Document31	Similarity: 0.04
Document47, Document9	Similarity: 0.02
Document47, Document8	Similarity: 0.04
Document47, Document7	Similarity: 0.07
Document47, Document6	Similarity: 0.07
Document47, Document5	Similarity: 0.03
Document47, Document4	Similarity: 0.02
Document47, Document3	Similarity: 0.05
Document47, Document2	Similarity: 0.04
Document47, Document1	Similarity: 0.04
Document47, Document29	Similarity: 0.06
Document47, Document27	Similarity: 0.15
Document47, Document28	Similarity: 0.05
Document48, Document45	Similarity: 0.06
Document48, Document46	Similarity: 0.06
Document48, Document43	Similarity: 0.08
Document48, Document44	Similarity: 0.03
Document48, Document41	Similarity: 0.07
Document48, Document42	Similarity: 0.08
Document48, Document40	Similarity: 0.04
Document48, Document38	Similarity: 0.10
Document48, Document39	Similarity: 0.04
Document48, Document36	Similarity: 0.07
Document48, Document37	Similarity: 0.06
Document48, Document34	Similarity: 0.08
Document48, Document35	Similarity: 0.03
Document48, Document32	Similarity: 0.06
Document48, Document33	Similarity: 1.00
Document48, Document30	Similarity: 0.06
Document48, Document31	Similarity: 0.06
Document48, Document9	Similarity: 0.03
Document48, Document8	Similarity: 0.07
Document48, Document7	Similarity: 0.06
Document48, Document6	Similarity: 0.07
Document48, Document5	Similarity: 0.07
Document48, Document4	Similarity: 0.04
Document48, Document3	Similarity: 0.05
Document48, Document2	Similarity: 0.03
Document48, Document1	Similarity: 0.04
Document48, Document29	Similarity: 0.03
Document48, Document27	Similarity: 0.08
Document48, Document28	Similarity: 0.08
Document45, Document46	Similarity: 0.01
Document45, Document43	Similarity: 0.05
Document45, Document44	Similarity: 0.04
Document45, Document41	Similarity: 0.04
Document45, Document42	Similarity: 0.08
Document45, Document40	Similarity: 0.09
Document45, Document38	Similarity: 0.07
Document45, Document39	Similarity: 0.03
Document45, Document36	Similarity: 0.05
Document45, Document37	Similarity: 0.01
Document45, Document34	Similarity: 0.03
Document45, Document35	Similarity: 0.03
Document45, Document32	Similarity: 0.09
Document45, Document33	Similarity: 0.06
Document45, Document30	Similarity: 1.00
Document45, Document31	Similarity: 0.01
Document45, Document9	Similarity: 0.05
Document45, Document8	Similarity: 0.07
Document45, Document7	Similarity: 0.06
Document45, Document6	Similarity: 0.04
Document45, Document5	Similarity: 0.08
Document45, Document4	Similarity: 0.02
Document45, Document3	Similarity: 0.06
Document45, Document2	Similarity: 0.04
Document45, Document1	Similarity: 0.02
Document45, Document29	Similarity: 0.04
Document45, Document27	Similarity: 0.08
Document45, Document28	Similarity: 0.05
Document46, Document43	Similarity: 0.07
Document46, Document44	Similarity: 0.04
Document46, Document41	Similarity: 0.04
Document46, Document42	Similarity: 0.04
Document46, Document40	Similarity: 0.05
Document46, Document38	Similarity: 0.11
Document46, Document39	Similarity: 0.04
Document46, Document36	Similarity: 0.08
Document46, Document37	Similarity: 0.07
Document46, Document34	Similarity: 0.06
Document46, Document35	Similarity: 0.07
Document46, Document32	Similarity: 0.04
Document46, Document33	Similarity: 0.06
Document46, Document30	Similarity: 0.01
Document46, Document31	Similarity: 1.00
Document46, Document9	Similarity: 0.01
Document46, Document8	Similarity: 0.04
Document46, Document7	Similarity: 0.07
Document46, Document6	Similarity: 0.08
Document46, Document5	Similarity: 0.02
Document46, Document4	Similarity: 0.05
Document46, Document3	Similarity: 0.04
Document46, Document2	Similarity: 0.05
Document46, Document1	Similarity: 0.03
Document46, Document29	Similarity: 0.04
Document46, Document27	Similarity: 0.04
Document46, Document28	Similarity: 0.07
Document43, Document44	Similarity: 0.05
Document43, Document41	Similarity: 0.07
Document43, Document42	Similarity: 0.05
Document43, Document40	Similarity: 0.06
Document43, Document38	Similarity: 0.15
Document43, Document39	Similarity: 0.06
Document43, Document36	Similarity: 0.11
Document43, Document37	Similarity: 0.09
Document43, Document34	Similarity: 0.14
Document43, Document35	Similarity: 0.03
Document43, Document32	Similarity: 0.05
Document43, Document33	Similarity: 0.08
Document43, Document30	Similarity: 0.05
Document43, Document31	Similarity: 0.07
Document43, Document9	Similarity: 0.03
Document43, Document8	Similarity: 0.06
Document43, Document7	Similarity: 0.03
Document43, Document6	Similarity: 0.07
Document43, Document5	Similarity: 0.04
Document43, Document4	Similarity: 0.03
Document43, Document3	Similarity: 0.03
Document43, Document2	Similarity: 0.06
Document43, Document1	Similarity: 0.04
Document43, Document29	Similarity: 0.05
Document43, Document27	Similarity: 0.05
Document43, Document28	Similarity: 1.00
Document44, Document41	Similarity: 0.05
Document44, Document42	Similarity: 0.01
Document44, Document40	Similarity: 0.09
Document44, Document38	Similarity: 0.05
Document44, Document39	Similarity: 0.13
Document44, Document36	Similarity: 0.08
Document44, Document37	Similarity: 0.04
Document44, Document34	Similarity: 0.05
Document44, Document35	Similarity: 0.06
Document44, Document32	Similarity: 0.06
Document44, Document33	Similarity: 0.03
Document44, Document30	Similarity: 0.04
Document44, Document31	Similarity: 0.04
Document44, Document9	Similarity: 0.05
Document44, Document8	Similarity: 0.08
Document44, Document7	Similarity: 0.07
Document44, Document6	Similarity: 0.05
Document44, Document5	Similarity: 0.03
Document44, Document4	Similarity: 0.05
Document44, Document3	Similarity: 0.02
Document44, Document2	Similarity: 0.03
Document44, Document1	Similarity: 0.02
Document44, Document29	Similarity: 1.00
Document44, Document27	Similarity: 0.01
Document44, Document28	Similarity: 0.05
Document41, Document42	Similarity: 0.03
Document41, Document40	Similarity: 0.11
Document41, Document38	Similarity: 0.09
Document41, Document39	Similarity: 0.05
Document41, Document36	Similarity: 0.10
Document41, Document37	Similarity: 0.05
Document41, Document34	Similarity: 0.07
Document41, Document35	Similarity: 0.04
Document41, Document32	Similarity: 0.05
Document41, Document33	Similarity: 0.07
Document41, Document30	Similarity: 0.04
Document41, Document31	Similarity: 0.04
Document41, Document9	Similarity: 0.05
Document41, Document8	Similarity: 0.08
Document41, Document7	Similarity: 0.06
Document41, Document6	Similarity: 0.14
Document41, Document5	Similarity: 0.05
Document41, Document4	Similarity: 0.04
Document41, Document3	Similarity: 0.10
Document41, Document2	Similarity: 0.05
Document41, Document1	Similarity: 0.04
Document41, Document29	Similarity: 0.05
Document41, Document27	Similarity: 0.03
Document41, Document28	Similarity: 0.07
Document42, Document40	Similarity: 0.07
Document42, Document38	Similarity: 0.04
Document42, Document39	Similarity: 0.03
Document42, Document36	Similarity: 0.04
Document42, Document37	Similarity: 0.04
Document42, Document34	Similarity: 0.08
Document42, Document35	Similarity: 0.03
Document42, Document32	Similarity: 0.15
Document42, Document33	Similarity: 0.08
Document42, Document30	Similarity: 0.08
Document42, Document31	Similarity: 0.04
Document42, Document9	Similarity: 0.03
Document42, Document8	Similarity: 0.03
Document42, Document7	Similarity: 0.04
Document42, Document6	Similarity: 0.03
Document42, Document5	Similarity: 0.06
Document42, Document4	Similarity: 0.02
Document42, Document3	Similarity: 0.06
Document42, Document2	Similarity: 0.03
Document42, Document1	Similarity: 0.03
Document42, Document29	Similarity: 0.01
Document42, Document27	Similarity: 1.00
Document42, Document28	Similarity: 0.05
Document40, Document38	Similarity: 0.08
Document40, Document39	Similarity: 0.04
Document40, Document36	Similarity: 0.10
Document40, Document37	Similarity: 0.04
Document40, Document34	Similarity: 0.09
Document40, Document35	Similarity: 0.10
Document40, Document32	Similarity: 0.10
Document40, Document33	Similarity: 0.04
Document40, Document30	Similarity: 0.09
Document40, Document31	Similarity: 0.05
Document40, Document9	Similarity: 0.05
Document40, Document8	Similarity: 0.13
Document40, Document7	Similarity: 0.09
Document40, Document6	Similarity: 0.06
Document40, Document5	Similarity: 0.03
Document40, Document4	Similarity: 0.06
Document40, Document3	Similarity: 0.10
Document40, Document2	Similarity: 0.04
Document40, Document1	Similarity: 0.07
Document40, Document29	Similarity: 0.09
Document40, Document27	Similarity: 0.07
Document40, Document28	Similarity: 0.06
Document38, Document39	Similarity: 0.07
Document38, Document36	Similarity: 0.14
Document38, Document37	Similarity: 0.06
Document38, Document34	Similarity: 0.10
Document38, Document35	Similarity: 0.03
Document38, Document32	Similarity: 0.04
Document38, Document33	Similarity: 0.10
Document38, Document30	Similarity: 0.07
Document38, Document31	Similarity: 0.11
Document38, Document9	Similarity: 0.04
Document38, Document8	Similarity: 0.05
Document38, Document7	Similarity: 0.05
Document38, Document6	Similarity: 0.07
Document38, Document5	Similarity: 0.06
Document38, Document4	Similarity: 0.05
Document38, Document3	Similarity: 0.05
Document38, Document2	Similarity: 0.05
Document38, Document1	Similarity: 0.04
Document38, Document29	Similarity: 0.05
Document38, Document27	Similarity: 0.04
Document38, Document28	Similarity: 0.15
Document39, Document36	Similarity: 0.06
Document39, Document37	Similarity: 0.05
Document39, Document34	Similarity: 0.06
Document39, Document35	Similarity: 0.03
Document39, Document32	Similarity: 0.03
Document39, Document33	Similarity: 0.04
Document39, Document30	Similarity: 0.03
Document39, Document31	Similarity: 0.04
Document39, Document9	Similarity: 0.03
Document39, Document8	Similarity: 0.05
Document39, Document7	Similarity: 0.04
Document39, Document6	Similarity: 0.07
Document39, Document5	Similarity: 0.04
Document39, Document4	Similarity: 0.03
Document39, Document3	Similarity: 0.06
Document39, Document2	Similarity: 0.03
Document39, Document1	Similarity: 0.02
Document39, Document29	Similarity: 0.13
Document39, Document27	Similarity: 0.03
Document39, Document28	Similarity: 0.06
Document36, Document37	Similarity: 0.10
Document36, Document34	Similarity: 0.05
Document36, Document35	Similarity: 0.04
Document36, Document32	Similarity: 0.04
Document36, Document33	Similarity: 0.07
Document36, Document30	Similarity: 0.05
Document36, Document31	Similarity: 0.08
Document36, Document9	Similarity: 0.04
Document36, Document8	Similarity: 0.10
Document36, Document7	Similarity: 0.07
Document36, Document6	Similarity: 0.12
Document36, Document5	Similarity: 0.06
Document36, Document4	Similarity: 0.03
Document36, Document3	Similarity: 0.07
Document36, Document2	Similarity: 0.06
Document36, Document1	Similarity: 0.08
Document36, Document29	Similarity: 0.08
Document36, Document27	Similarity: 0.04
Document36, Document28	Similarity: 0.11
Document37, Document34	Similarity: 0.04
Document37, Document35	Similarity: 0.03
Document37, Document32	Similarity: 0.04
Document37, Document33	Similarity: 0.06
Document37, Document30	Similarity: 0.01
Document37, Document31	Similarity: 0.07
Document37, Document9	Similarity: 0.03
Document37, Document8	Similarity: 0.05
Document37, Document7	Similarity: 0.09
Document37, Document6	Similarity: 0.11
Document37, Document5	Similarity: 0.02
Document37, Document4	Similarity: 0.02
Document37, Document3	Similarity: 0.04
Document37, Document2	Similarity: 0.04
Document37, Document1	Similarity: 0.05
Document37, Document29	Similarity: 0.04
Document37, Document27	Similarity: 0.04
Document37, Document28	Similarity: 0.09
Document34, Document35	Similarity: 0.03
Document34, Document32	Similarity: 0.03
Document34, Document33	Similarity: 0.08
Document34, Document30	Similarity: 0.03
Document34, Document31	Similarity: 0.06
Document34, Document9	Similarity: 0.07
Document34, Document8	Similarity: 0.12
Document34, Document7	Similarity: 0.06
Document34, Document6	Similarity: 0.08
Document34, Document5	Similarity: 0.07
Document34, Document4	Similarity: 0.02
Document34, Document3	Similarity: 0.07
Document34, Document2	Similarity: 0.03
Document34, Document1	Similarity: 0.04
Document34, Document29	Similarity: 0.05
Document34, Document27	Similarity: 0.08
Document34, Document28	Similarity: 0.14
Document35, Document32	Similarity: 0.06
Document35, Document33	Similarity: 0.03
Document35, Document30	Similarity: 0.03
Document35, Document31	Similarity: 0.07
Document35, Document9	Similarity: 0.02
Document35, Document8	Similarity: 0.04
Document35, Document7	Similarity: 0.13
Document35, Document6	Similarity: 0.02
Document35, Document5	Similarity: 0.02
Document35, Document4	Similarity: 0.04
Document35, Document3	Similarity: 0.07
Document35, Document2	Similarity: 0.01
Document35, Document1	Similarity: 0.04
Document35, Document29	Similarity: 0.06
Document35, Document27	Similarity: 0.03
Document35, Document28	Similarity: 0.03
Document32, Document33	Similarity: 0.06
Document32, Document30	Similarity: 0.09
Document32, Document31	Similarity: 0.04
Document32, Document9	Similarity: 0.02
Document32, Document8	Similarity: 0.04
Document32, Document7	Similarity: 0.07
Document32, Document6	Similarity: 0.07
Document32, Document5	Similarity: 0.03
Document32, Document4	Similarity: 0.02
Document32, Document3	Similarity: 0.05
Document32, Document2	Similarity: 0.04
Document32, Document1	Similarity: 0.04
Document32, Document29	Similarity: 0.06
Document32, Document27	Similarity: 0.15
Document32, Document28	Similarity: 0.05
Document33, Document30	Similarity: 0.06
Document33, Document31	Similarity: 0.06
Document33, Document9	Similarity: 0.03
Document33, Document8	Similarity: 0.07
Document33, Document7	Similarity: 0.06
Document33, Document6	Similarity: 0.07
Document33, Document5	Similarity: 0.07
Document33, Document4	Similarity: 0.04
Document33, Document3	Similarity: 0.05
Document33, Document2	Similarity: 0.03
Document33, Document1	Similarity: 0.04
Document33, Document29	Similarity: 0.03
Document33, Document27	Similarity: 0.08
Document33, Document28	Similarity: 0.08
Document30, Document31	Similarity: 0.01
Document30, Document9	Similarity: 0.05
Document30, Document8	Similarity: 0.07
Document30, Document7	Similarity: 0.06
Document30, Document6	Similarity: 0.04
Document30, Document5	Similarity: 0.08
Document30, Document4	Similarity: 0.02
Document30, Document3	Similarity: 0.06
Document30, Document2	Similarity: 0.04
Document30, Document1	Similarity: 0.02
Document30, Document29	Similarity: 0.04
Document30, Document27	Similarity: 0.08
Document30, Document28	Similarity: 0.05
Document31, Document9	Similarity: 0.01
Document31, Document8	Similarity: 0.04
Document31, Document7	Similarity: 0.07
Document31, Document6	Similarity: 0.08
Document31, Document5	Similarity: 0.02
Document31, Document4	Similarity: 0.05
Document31, Document3	Similarity: 0.04
Document31, Document2	Similarity: 0.05
Document31, Document1	Similarity: 0.03
Document31, Document29	Similarity: 0.04
Document31, Document27	Similarity: 0.04
Document31, Document28	Similarity: 0.07
Document9, Document8	Similarity: 0.07
Document9, Document7	Similarity: 0.06
Document9, Document6	Similarity: 0.07
Document9, Document5	Similarity: 0.10
Document9, Document4	Similarity: 0.04
Document9, Document3	Similarity: 0.07
Document9, Document2	Similarity: 0.08
Document9, Document1	Similarity: 0.02
Document9, Document29	Similarity: 0.05
Document9, Document27	Similarity: 0.03
Document9, Document28	Similarity: 0.03
Document8, Document7	Similarity: 0.10
Document8, Document6	Similarity: 0.14
Document8, Document5	Similarity: 0.04
Document8, Document4	Similarity: 0.06
Document8, Document3	Similarity: 0.08
Document8, Document2	Similarity: 0.05
Document8, Document1	Similarity: 0.03
Document8, Document29	Similarity: 0.08
Document8, Document27	Similarity: 0.03
Document8, Document28	Similarity: 0.06
Document7, Document6	Similarity: 0.13
Document7, Document5	Similarity: 0.03
Document7, Document4	Similarity: 0.07
Document7, Document3	Similarity: 0.09
Document7, Document2	Similarity: 0.08
Document7, Document1	Similarity: 0.04
Document7, Document29	Similarity: 0.07
Document7, Document27	Similarity: 0.04
Document7, Document28	Similarity: 0.03
Document6, Document5	Similarity: 0.04
Document6, Document4	Similarity: 0.03
Document6, Document3	Similarity: 0.06
Document6, Document2	Similarity: 0.07
Document6, Document1	Similarity: 0.04
Document6, Document29	Similarity: 0.05
Document6, Document27	Similarity: 0.03
Document6, Document28	Similarity: 0.07
Document5, Document4	Similarity: 0.03
Document5, Document3	Similarity: 0.09
Document5, Document2	Similarity: 0.08
Document5, Document1	Similarity: 0.02
Document5, Document29	Similarity: 0.03
Document5, Document27	Similarity: 0.06
Document5, Document28	Similarity: 0.04
Document4, Document3	Similarity: 0.05
Document4, Document2	Similarity: 0.06
Document4, Document1	Similarity: 0.04
Document4, Document29	Similarity: 0.05
Document4, Document27	Similarity: 0.02
Document4, Document28	Similarity: 0.03
Document3, Document2	Similarity: 0.05
Document3, Document1	Similarity: 0.03
Document3, Document29	Similarity: 0.02
Document3, Document27	Similarity: 0.06
Document3, Document28	Similarity: 0.03
Document2, Document1	Similarity: 0.03
Document2, Document29	Similarity: 0.03
Document2, Document27	Similarity: 0.03
Document2, Document28	Similarity: 0.06
Document1, Document29	Similarity: 0.02
Document1, Document27	Similarity: 0.03
Document1, Document28	Similarity: 0.04
Document29, Document27	Similarity: 0.01
Document29, Document28	Similarity: 0.05
Document27, Document28	Similarity: 0.05


```
## License
This project is licensed under the MIT License.

## Contact
For questions, contact the course instructor or open an issue in the repository.
