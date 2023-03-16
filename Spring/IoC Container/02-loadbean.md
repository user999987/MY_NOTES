.gradle/caches/modules-2/files-2.1/org.springframework/spring-context/5.3.10/8d6a3e906fee80bad904bae643973781cd4cc881/spring-context-5.3.10-sources.jar!/org/springframework/context/support/AbstractApplicationContext.java
```java
@Override
public void refresh() throws BeansException, IllegalStateException {
    synchronized (this.startupShutdownMonitor) {
        StartupStep contextRefresh = this.applicationStartup.start("spring.context.refresh");

        // Prepare this context for refreshing.
        // 包括启动设置启动时间，是否激活标志位，初始化属性源配置
        prepareRefresh();

        // Tell the subclass to refresh the internal bean factory.
        /**
         * 初始化 BeanFactory，解析xml格式的配置文件. xml格式的配置，是在这个方法中扫描到 beanDefinitionMap 中的 具体如下
         * .gradle/caches/modules-2/files-2.1/org.springframework/spring-web/5.3.10/63a2c8efa9006c0f14743cbcaab2c62a43ec5f0e/spring-web-5.3.10-sources.jar!/org/springframework/web/context/support/XmlWebApplicationContext.java
         * org.springframework.web.context.support.XmlWebApplicationContext#loadBeanDefinitions(org.springframework.beans.factory.support.DefaultListableBeanFactory) 
         * 中会创建一个 XmlBeanDefinitionReader来解析 xml 文件
         * 会把 bean.xml 解析成一个InputStream，然后再解析成 document object model(一个树状结构，xml和html本身就是结构化，所以可转化)
         * 按照 DOM， 从 root 开始进行解析，判断节点是 bean or beans or import等
         * 如果是 bean 就把解析到的信息包装成 beanDefinitionHolder, 然后调用 DefaultListablebeanFactory 的注册方法将 bean 放到 beanDefinitionMap中
        **/
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();

        // Prepare the bean factory for use in this context.
        // 给 BeanFactory 设置属性,添加后置处理器等
        prepareBeanFactory(beanFactory);

        try {
            // Allows post-processing of the bean factory in context subclasses.
            // 空方法 留给子类定义
            // 
            postProcessBeanFactory(beanFactory);

            StartupStep beanPostProcess = this.applicationStartup.start("spring.context.beans.post-process");
            // Invoke factory processors registered as beans in the context.
            /**
             * 完成对bean的扫描，将 class 变成 beanDefinition 并将 beanDefinition存到 map 中
             * 该方法在 spring 的环境中执行已经被注册的 factory processors
             * 执行自定义的processBeanFactory
             *
             * 这个方法中 bean 的注入分为三种
             * 一. 普通bean: @Component 注解的 bean
             * spring 自己的类，不借助 spring扫描，会直接放到 beanDefinitionMap
             *
             * 1. 获取所有的beanFactoryPostProcessor
             * 2. 执行 bean后置处理器的postPorcessBeanFactory(configurationClassPostPorcessor), 
             *  该方法会把 beanFactory 作为参数传到方法
             * 3. 从 beanFactory中获取到所有的beanName (可打开断点看下 org.springframework.context.annotation.ConfigurationClasspostporcessor#processConfigbeanDefinitions)
             * 4. 然后将所有的 bean 包装成 beanDefinitionHolder,在后面又根据 beanName和 bean的metadata包装成
             *  了 Configurationclass
             * 5. 把所有包含 @componentScan 的类取出来, 遍历每一个 componentScan, 调用 
             * ClassPathBeanDenifitionScanner.doScan(basePackages)方法
             * 6. 在 doScan 方法中, 会遍历 basePackages, 因为一个ComponentScan中可以配置多个要扫描的包
             * 7. 获取每个包下面的 *.class 文件, registerBeanDefinition(definitionHolder, this.registry)
             *  这个方法底层就是调用 org.springframework.beans.factory.support.DefaultListableBeanFactory#registerBeanDefinition 方法 把当前 bean put 到 beanDefinitionMap中
             *
             * 二. 通过 @Import 注解注入的 bean
             *  ImportBeanDefinitionRegistrar
             *  ImportSelector
             *
             * 三. @Bean注解
             *
             *
             * spring 在把 bean注入到 beanDefinitionMaps的同时，会将当前beanName 添加到一个叫 beanDefinitionNames的 list, 这个list和beanDefinitionMap 是同时进行添加的
             *  这个list 在后面实例化bean的时候有用到, spring是遍历这个list, 拿到每个beanName之后, 从beanDefinitionMap中取到对应的 beanDefinition
             */
            invokeBeanFactoryPostProcessors(beanFactory);

            // Register bean processors that intercept bean creation.
            /**
            *  bean 后置处理器 允许我们在工厂里所有的bean被加载进来后但是还没初始化前，对所有bean的属性进行修改也可以add属性值
            *
            *  在方法里 会先把 beanPostPorcessor 进行分类, 然后按照 beanPostProcessor的 name 从
            *  spring 容器中获取 bean对象, 如果 容器中没有 就创建. 所以 如果一个 beanDefinition 是
            *  后置处理器, 会在这里进行实例化, 然后存放到单实例池中
            *  然后在调用 beanFactory.addBeanPostProcessor(postProcessor)
            *  把所有的 beanPostProcessor 放到了 beanPostProcessors 中, 在后面初始化 bean 的时候, 
            *  如果需要调用后置处理器 就会遍历这个list
            */
            registerBeanPostProcessors(beanFactory);
            beanPostProcess.end();

            // Initialize message source for this context.
            initMessageSource();

            // Initialize event multicaster for this context.
            initApplicationEventMulticaster();

            // Initialize other special beans in specific context subclasses.
            /**
            * 这是一个空方法， 在 springboot中, 如果集成了 Tomcat, 会在这里 
            *   new Tomcat()
            *   new DispatcherServlet()
            */
            onRefresh();

            // Check for listener beans and register them.
            registerListeners();

            // Instantiate all remaining (non-lazy-init) singletons.
            // 完成对 bean的实例化 主要的功能都在这里
            finishBeanFactoryInitialization(beanFactory);

            // Last step: publish corresponding event.
            finishRefresh();
        }

        catch (BeansException ex) {
            if (logger.isWarnEnabled()) {
                logger.warn("Exception encountered during context initialization - " +
                        "cancelling refresh attempt: " + ex);
            }

            // Destroy already created singletons to avoid dangling resources.
            destroyBeans();

            // Reset 'active' flag.
            cancelRefresh(ex);

            // Propagate exception to caller.
            throw ex;
        }

        finally {
            // Reset common introspection caches in Spring's core, since we
            // might not ever need metadata for singleton beans anymore...
            resetCommonCaches();
            contextRefresh.end();
        }
    }
}
```
在refresh方法中，完成bean的初始化、动态代理、放入容器等操作；我们着重来说spring是如何扫描bean的，invokeBeanFactoryPostProcessors(beanFactory);在该方法中，完成了对所有要注入到spring容器中的业务类的扫描，将业务类转换成beanDefinition，并存入了BeanDefinitionMap中，这就是该方法完成的操作

在 invokeBeanFactoryPostProcessors 中 有一行代码 `invokeBeanDefinitionRegistryPostProcessors(currentRegistryProcessors, registry, beanFactory.getApplicationStartup())`, 此代码是执行BeanDefinitionRegistryPostProcessor接口实现类的 postProcessBeanDefinitionRegistry() 方法

从spring启动到现在, beanDefinitionMap中的所有 bean, BeanDefinitionRegistryPostProcessor接口的实现类只有一个, `ConfigurationClassPostProcessor`. 

执行 invokeBeanDefinitionRegistryPostProcessors 的时候会执行 ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry(), 其中最重要的是 org.springframework.context.annotation.ConfigurationClassPostProcessor#processConfigBeanDefinitions

```java
public void processConfigBeanDefinitions(BeanDefinitionRegistry registry) {
        /**
         *  这个list用来保存 
         *  添加了 @Configuration 的类
         *  添加了 @Component 或者 @ComponentScan 或者 @Import 或者 @ImportResource 注解的类
         *
         *  区别是 @Configuration 对应的 ConfigurationClass是 full, 否则是 lite
         * 
         *  正常情况下 第一次进入到这里的时候 只有配置类一个 bean. 因为如果第一次你如刀这里的话, beanDefinitionMap中只有配置类这一个是我们程序员提供的 业务类, 其他都是spring自带的后置处理器     
         */
		List<BeanDefinitionHolder> configCandidates = new ArrayList<>();
        // 获取在 AnnotatedBeanDefinitionReader()中注入的 spring 自己的 beanPostProcessor
		String[] candidateNames = registry.getBeanDefinitionNames();

		for (String beanName : candidateNames) {
			BeanDefinition beanDef = registry.getBeanDefinition(beanName);
            /**
            *   如果 bean 是配置类, confugurationClass 就是 full 否则就是 lite
            *   这里 如果当前 bean 的 configurationClass 属性已经被设置值了, 说明当前 bean已经被解析过了 
            **/
			if (beanDef.getAttribute(ConfigurationClassUtils.CONFIGURATION_CLASS_ATTRIBUTE) != null) {
				if (logger.isDebugEnabled()) {
					logger.debug("Bean definition has already been processed as a configuration class: " + beanDef);
				}
			}
            // 校验 bean 是否包含 @Configureation 也就是校验 bean是哪种配置类?注解? 还是普通的配置类
			else if (ConfigurationClassUtils.checkConfigurationClassCandidate(beanDef, this.metadataReaderFactory)) {
				configCandidates.add(new BeanDefinitionHolder(beanDef, beanName));
			}
		}

		// Return immediately if no @Configuration classes were found
		if (configCandidates.isEmpty()) {
			return;
		}

		// Sort by previously determined @Order value, if applicable
		configCandidates.sort((bd1, bd2) -> {
			int i1 = ConfigurationClassUtils.getOrder(bd1.getBeanDefinition());
			int i2 = ConfigurationClassUtils.getOrder(bd2.getBeanDefinition());
			return Integer.compare(i1, i2);
		});

		// Detect any custom bean name generation strategy supplied through the enclosing application context
		SingletonBeanRegistry sbr = null;
		if (registry instanceof SingletonBeanRegistry) {
			sbr = (SingletonBeanRegistry) registry;
			if (!this.localBeanNameGeneratorSet) {
				BeanNameGenerator generator = (BeanNameGenerator) sbr.getSingleton(
						AnnotationConfigUtils.CONFIGURATION_BEAN_NAME_GENERATOR);
				if (generator != null) {
					this.componentScanBeanNameGenerator = generator;
					this.importBeanNameGenerator = generator;
				}
			}
		}

		if (this.environment == null) {
			this.environment = new StandardEnvironment();
		}

		// Parse each @Configuration class
        // 实例化 ConfigurationClassParser 是为了解析各个配置类
		ConfigurationClassParser parser = new ConfigurationClassParser(
				this.metadataReaderFactory, this.problemReporter, this.environment,
				this.resourceLoader, this.componentScanBeanNameGenerator, registry);
        /**
         *  这两个 set 主要是为了去重
         *  正常情况下 下面的 do...while 循环中 只会循环处理所有的配类, 因为目前为止还没有普通的bean添加到beanDefinitionmap中  
         */
		Set<BeanDefinitionHolder> candidates = new LinkedHashSet<>(configCandidates);
		Set<ConfigurationClass> alreadyParsed = new HashSet<>(configCandidates.size());
		do {
			StartupStep processConfig = this.applicationStartup.start("spring.context.config-classes.parse");
            /**
             *  这里的 candidates 的个数是由项目中 配置文件的数量来决定的(或者说加了@Configuration或者@ComponentScan或者@Component注解的类)
             */
			parser.parse(candidates);
			parser.validate();

			Set<ConfigurationClass> configClasses = new LinkedHashSet<>(parser.getConfigurationClasses());
			configClasses.removeAll(alreadyParsed);

			// Read the model and create bean definitions based on its content
			if (this.reader == null) {
				this.reader = new ConfigurationClassBeanDefinitionReader(
						registry, this.sourceExtractor, this.resourceLoader, this.environment,
						this.importBeanNameGenerator, parser.getImportRegistry());
			}
            /**
             *  这里的configClasses 就是parse方法中, 对import注解进行处理时存入的
             *  这个方法里面 完成了对 ImportSelector 和 ImportBeanDefinitionRegistrar 注入的 bean进行初始化
             */
			this.reader.loadBeanDefinitions(configClasses);
			alreadyParsed.addAll(configClasses);
			processConfig.tag("classCount", () -> String.valueOf(configClasses.size())).end();

			candidates.clear();
			if (registry.getBeanDefinitionCount() > candidateNames.length) {
				String[] newCandidateNames = registry.getBeanDefinitionNames();
				Set<String> oldCandidateNames = new HashSet<>(Arrays.asList(candidateNames));
				Set<String> alreadyParsedClasses = new HashSet<>();
				for (ConfigurationClass configurationClass : alreadyParsed) {
					alreadyParsedClasses.add(configurationClass.getMetadata().getClassName());
				}
				for (String candidateName : newCandidateNames) {
					if (!oldCandidateNames.contains(candidateName)) {
						BeanDefinition bd = registry.getBeanDefinition(candidateName);
						if (ConfigurationClassUtils.checkConfigurationClassCandidate(bd, this.metadataReaderFactory) &&
								!alreadyParsedClasses.contains(bd.getBeanClassName())) {
							candidates.add(new BeanDefinitionHolder(bd, candidateName));
						}
					}
				}
				candidateNames = newCandidateNames;
			}
		}
		while (!candidates.isEmpty());

		// Register the ImportRegistry as a bean in order to support ImportAware @Configuration classes
		if (sbr != null && !sbr.containsSingleton(IMPORT_REGISTRY_BEAN_NAME)) {
			sbr.registerSingleton(IMPORT_REGISTRY_BEAN_NAME, parser.getImportRegistry());
		}

		if (this.metadataReaderFactory instanceof CachingMetadataReaderFactory) {
			// Clear cache in externally provided MetadataReaderFactory; this is a no-op
			// for a shared cache since it'll be cleared by the ApplicationContext.
			((CachingMetadataReaderFactory) this.metadataReaderFactory).clearCache();
		}
	}
```
以上方法完成了以下操作:
1. 从 beanDefinitionMap中获取到添加了以下注解的类 @Configuration, @ComponentScan, @Component, @Import, @ImportResource
2. 遍历获取到的bean, 解析bean中的 @ComponentScan 注解,根据该注解, 将包下的bean, 转换成BeanDefinition, 并放入到BeanDefinitionMap中
3. 处理类上通过@Import引入的ImportSelector接口的实现类和ImportBeanDefinitionRegistry接口的实现类
4. 处理@Bean注解引入的bean
5. 处理@ImportResource注解