# **PROJECT: UTILIZING COMPUTER VISION AND SUPPORT VECTOR MACHINE FOR SITTING POSTURE ASSESSMENT**

## **ABSTRACT**

Poor sitting posture is an urgent problem on a global scale, driven by the rising prevalence of sedentary activities such as prolonged computer use. Poor sitting posture leads to work-related musculoskeletal disorders such as carpal tunnel, back injury, and back pain; cardiovascular diseases; and even permanent health damage, resulting in expensive treatments for both employers and employees. Many posture monitoring technologies rely on pressure and inertia sensors, and while these instruments are accurate, they are intrusive, expensive, and require a specialized setup, making them unsuitable for widespread deployment. Posture monitoring using cameras offers an unintrusive, cost-effective, and convenient solution while maintaining high accuracy; however, current methods are challenged by high computational demands, sensitivity to environmental conditions, and inconvenient camera placements. This paper presents a novel camera-based approach, designed to be deployed on a laptop using the built-in camera without any additional setup. First, we synthesize previous works to develop a comprehensive classification system for “correct” and “incorrect” posture. Subsequently, four numerical ratios between distances of key joint coordinates calibrated for individual users are extracted as input data for a Support Vector Machine (SVM) model to perform posture classification. By using numerical data rather than images of depth maps as input for posture-classification models, the proposed method significantly reduces the computational requirement as well as minimizes the effect of environmental variables. This approach addresses existing challenges in camera-based posture monitoring and offers a practical, efficient solution for real-time sitting posture assessment. Furthermore, this paper also discusses utilizing the lightweight computational load of the SVM model for deployment on edge-AI modules, enabling a portable and robust sitting posture assessment system.
## **I. Preliminary literature review**

### **1. Current situation on bad posture**

**1.1. In Vietnam**

Bad posture is a pressing issue among Vietnamese, especially in students. It is the main factor of scoliois, which the Commission for Information and Education reported to affect 1.3% to 36.33% of the students in major cities in Vietnam in 2022. This is an alarming rise from 7.4% in 2019, and the number is expected to continue to increase in the future.

**1.2. Around the world**

Bad posture is also an urgent problem on the global scale. Due to the pandemic, the time people spent in sedentary activities such as sitting working on a computer for a long period has increased considerably. According to Vermander et al. (2024), nowadays people spend more than half of their daily hours in a seated position, reaching up to 85% of their hours in the case of people with low mobility. Nadeem M. et al. (2024) stated an average office worker in today’s world uses up to 75% of their day sitting, with over half of that time occurring during extended periods of almost complete inactivity. This will enventually lead to to work-related musculoskeletal disorders (Rodrigues P. et al., 2022), cardio-vascular diseases (CVDs), metabolic syndrome, diabetes, and hypertension (Estrada J. et al., 2023) if the posture is not carefully monitored. Furthermore, poor posture causes musculoskeltal disorders such as carpal tunnel, back injury and back pain and also permanent damage to health, resulting in a great amount of expenses for treatments for both the employers and employee (Ding Z. et al., 2019). Several medical studies have proven that bad posture after long periods results in major back/neck problems (Kapoor R. et al., 2022), as multiple studies showed that 17.7–63% of soffice workers experienced neck pain, and 23–34% suffered from back pain (Estrada J. et al., 2023). As the number of people who will sit and work in front of a computer will increase in the future, and many of them do not have the knowledge on how to maintain proper posture (Kapoor R. et al., 2022) or are occupied with work to effectively adhere to ergronomics rules, _a need for efficient and convinient sitting posture monitor systems is evident._

### **2. A summary of current sitting posture monitor technology**

Two literature reviews on current sitting posture monitor system stood out due to the comprehensiveness during the preliminary literature review for this project; one by Vermander et al. (2024) and one by Nadeem et al. (2024). Here, the work of both authors are combined to establish the most complete overview of the technology.

According to Vermader et al. (2024), the main structure of the majority of sitting posture systems consists of 2 main components: the "monitoring system", which extracts postural data (joints coordinates, sitting pressures in different points, arm angles, etc), and the "intelligent anomaly detection", which uses the extracted data to classify the posture of the user in to class e.g. "normal" or "abnormal."

**2.1. Monitoring system**

As Vermander et al. (2024) suggested, there are 3 main groups of monitoring systems: 

(1) Systems located in environment: uses RGB cameras/infrared/depth camera/kietic camera and computer vision to extract data on the hips, shoulders, arms, etc. They are favoured due to fast and non-intrusive processing, but they are strongly dependent on the range of vision of the camera, their results could be affected by environmental conditions (e.g. lighting), and they raises concerns of privacy. Other technologies, but not as popular, include ultilizing RFID/Ultrasonic sensor and Sensor fusion (Nadeem et al., 2024)

(2) Systems located on users: uses wearable sensors, the most popular being internal sensors located along the spine or chest. ALthough small in size, they are uncomfortable and require specialist to perform complicated set-up procedures and data extraction. Their accuracy has not been compared to other methods.

(3) Systems located on assistance devices: uses sensors on chairs (e.g. restrictive transduction sensors, capicative sensors, piezo-electric sensors, pressure sensors, or force Sensing Sensors distributed as a mesh or as a flexible mat). Their accuracy has not been compared to other methodologies, and they are expensive, intrusive and also require specialized set-up.

**2.2. Intelligent anomaly detection techniques**

Intelligent anomaly detection techniques are divided into 2 groups. The first one, which is also the more popular one, is dubbed by Vermander et al. (2024) as "Traditional generalized technique", in which the definition of "correct posture" as "an upright spine, distributing the weight of the body evenly over the seat and backrest" is applied to every user regadless of physiology variance. Any posture that falls out of this group is considered false posture, and since this technique focus on a general, binary classification of posture, samples for classification are labeled either “normal” or “anomalous.” The second one, which is called the "New individualized approach technique," defined abnormal posture as deviations from the individual's typical pattern rather than a universal standard. To this end, individualized sitting postural pattern is characterized for each user, acknowledging that “normal/correct posture” varies based on the physiology of each person, and classification of postures includes various classes rather than only two. Notably, the "Traditional generalized technique" and "New individualized approach technique" consist of multiple methods.

**2.2.1. Traditional generalized technique:** There are 3 main methods for this technique.

(1) _Rule-based method:_ Based on prior knowledge or expert input, logical rules are set. These rules often include thresholds or conditions for what constitutes normal or anomalous behavior. The most popular method here is using a non-machine learning thresholding approach. This method has high simplicity, interpretatblity, low computational cost, but low robustness.

(2) _Statistical method:_ Data for normal and abnormal posture is gathered. Then, statistical techniques (logistic regression or K-nearest neighbors) are used to find the function best fit the data for normal and abnormal data, assuming that the data and the classification class have a functional relation. Classification for input data points are based on the probability of the input relative to the previously calculated function. This method has moderate simplicity, interpretability, moderate computational cost, but moderate robustness.

(3) _Intelligent method:_ Using machine learning (SVM, CNN, etc) for classification. This method has low simplicity, interpretatblity, high computational cost, but high robustness.

**2.2.2. New individualized technique:** There are 3 main methods for this technique.

(1)_ Supervised method:_ Train a model using labeled data for both normal and anomalous postures. The goal is to classify new samples into these predefined classes. Popular technologies include SVM, random forest, CNN, etc.

(2) _Semi-supervise method:_ Models trained using only normal data to define the expected behavior. Any deviation from the learned normality is flagged as anomalous. Popular technologies include one class SVM, KNN, etc.

(3) _Unsupervised method:_ No labels are provided. Anomalies are detected based on deviations from inherent patterns in the dataset. Popular technologies include K-means, PCA, etc.

**2.3. Integration with IoT for feed back alert**

Nadeem et al. (2024) remarked the growing trend of integrating IoT into posture monitoring systems to enhance the data extraction process, monitor energy consumption, and provide active feedback to users to improve their posture based on the detection results.

**2.4. Challenges**

Nadeem et al. (2024) highlight the primary challenges that different technologies for sitting posture monitoring system face, thus suggesting future research directions. For sensor-based systems, the paper point out the high cost, intrusiveness/discomfort, and requring specialized set-up as the main shortcomings, encouring future research to develop less intrusive and more ergonomic sensors (e.g., fabric-based or integrated into furniture), focus on low-power, cost-effective designs, and explore sensor fusion to combine strengths of different sensor types. For image-based systems, the challenges mentioned include dependency on favorable environmental conditions, such as consistent lighting; privacy concerns due to continuous video recording; as well as high computational demands for real-time processing and feature extraction. To this end, the paper suggest future research should focus on utilizing advanced AI techniques, such as deep learning, to improve robustness against lighting and occlusions and adopt privacy-preserving methods, like processing data on local devices or using anonymized features.

### **3. References**

Reference Here.

## **II. Problem statement and Contributions**

## **III. Project details**

### **1. Classification of "normal" and "abnormal" posture**

Since this project concerns only with the binary classification of postures (e.g. "normal" and "abnormal"), it is essential to establish a detailed definition of each posture type. In this project, we combine the classification technique of Ding Z. et al. (2019) and the definition of "good posture" in the work of Nadeem M. et al. (2024) and Kapoor R. et al. (2022).

Ding Z. et al. (2019) first classify different postures into 30 posture classes as combinations of the orientiation of the trunk (supine, erect, bend, and prone), the neck (look ahead, look down), and sitting orientations (turn left, lean left, middle, lean right, turn right, and turn back). Subsequently, they grouped various among of the 30 posture types into 2 classes: low-risk, and high-risk (Figure 1). The paper offers 2 more ways to classify postures, but this project will adopt this technique.










 


