IoC is also known as dependency injection (DI)

The BeanFactory provides the configuration framework and basic functionality, and the ApplicationContext (sub-interface of BeanFactory)adds more enterprise-specific functionality.

In Spring, the objects that form the backbone of your application and that are managed by the Spring IoC container are called beans. A bean is an object that is instantiated, assembled, and otherwise managed by a Spring IoC container

The interface org.springframework.context.ApplicationContext represents the Spring IoC container and is responsible for instantiating, configuring, and assembling the aforementioned beans. The container gets its instructions on what objects to instantiate, configure, and assemble by reading configuration metadata. The configuration metadata is represented in XML, Java annotations, or Java code.

Spring configuration consists of at least one and typically more than one bean definition that the container must manage. Java configuration typically uses @Bean-annotated methods within a @Configuration class.

Within the container itself, bean definitions are represented as BeanDefinition objects.
```kotlin
// get all bean names
context.beanDefinitionNames
```

ApplicationContext implementations also permit the registration of existing objects that are created outside the container (by users). `registerSingleton(..) and registerBeanDefinition(..)`

The recommended way to find out about the actual runtime type of a particular bean is a BeanFactory.getType call for the specified bean name.

### Setter-based Dependency Injection
```kotlin
class SimpleMovieLister {

    // a late-initialized property so that the Spring container can inject a MovieFinder
    lateinit var movieFinder: MovieFinder

    // business logic that actually uses the injected MovieFinder is omitted...
}
```

## Constructor-based or setter-based DI?
Since you can mix constructor-based and setter-based DI, it is a good rule of thumb to use constructors for mandatory dependencies and setter methods or configuration methods for optional dependencies. Note that use of the @Required annotation on a setter method can be used to make the property be a required dependency; however, constructor injection with programmatic validation of arguments is preferable.

The Spring team generally advocates constructor injection, as it lets you implement application components as immutable objects and ensures that required dependencies are not null. Furthermore, constructor-injected components are always returned to the client (calling) code in a fully initialized state. As a side note, a large number of constructor arguments is a bad code smell, implying that the class likely has too many responsibilities and should be refactored to better address proper separation of concerns.

Setter injection should primarily only be used for optional dependencies that can be assigned reasonable default values within the class. Otherwise, not-null checks must be performed everywhere the code uses the dependency. One benefit of setter injection is that setter methods make objects of that class amenable to reconfiguration or re-injection later. Management through JMX MBeans is therefore a compelling use case for setter injection.

Use the DI style that makes the most sense for a particular class. Sometimes, when dealing with third-party classes for which you do not have the source, the choice is made for you. For example, if a third-party class does not expose any setter methods, then constructor injection may be the only available form of DI.

org.springframework.context.support.AbstractApplicationContext.refresh() bean的加载入口

## Bean & Component
1. @Component注解表明一个类会作为组件类，并告知Spring要为这个类创建bean。
2. @Bean注解告诉Spring这个方法将会返回一个对象，这个对象要注册为Spring应用上下文中的bean。通常方法体中包含了最终产生bean实例的逻辑。
   
@Component（@Controller控制层、@Service业务层、@Repository持久层), 而用 @Component 对那些比较中立的类进行注释

那为什么有了@Compent,还需要@Bean呢？
如果你想要将第三方库中的组件装配到你的应用中，在这种情况下，是没有办法在它的类上添加@Component注解的，因此就不能使用自动化装配的方案了，但是我们可以使用@Bean,当然也可以使用XML配置。
```kotlin
@Bean
public Oneservice getService(status):
    case(status){
        when 1: return svc1()
        when 2: return svc2()
        when 3: return svc3()
    }
```
Cannot use Component to implement above.

## Autowired
@Autowired注解的意思就是，当Spring发现@Autowired注解时，将自动在代码上下文中找到和其匹配（默认是类型匹配）的Bean，并自动注入到相应的地方去。`@Autowired注解要去寻找的是一个Bean`
其作用是为了消除代码Java代码里面的getter/setter与bean属性中的property

## Resource
```java
@Service
public class Zoo
{
    @Resource(name = "tiger")
    private Tiger tiger;
    
    @Resource(type = Monkey.class)
    private Monkey monkey;
    
    public String toString()
    {
        return tiger + "\n" + monkey;
    }
```
这是详细一些的用法，说一下@Resource的装配顺序：

1. @Resource后面没有任何内容，默认通过name属性去匹配bean，找不到再按type去匹配

2. 指定了name或者type则根据指定的类型去匹配bean

3. 指定了name和type则根据指定的name和type去匹配bean，任何一个不匹配都将报错

然后，区分一下@Autowired和@Resource两个注解的区别：

1. @Autowired默认按照byType方式进行bean匹配，@Resource默认按照byName方式进行bean匹配

2. @Autowired是Spring的注解，@Resource是J2EE的注解，这个看一下导入注解的时候这两个注解的包名就一清二楚了

Spring属于第三方的，J2EE是Java自己的东西，因此，建议使用@Resource注解，以减少代码和Spring之间的耦合。