service is more like controller, biz looks like a service and entity place \
In the context of Kratos, a use case typically resides in the "biz" package and represents the core logic of the application. It defines the steps, rules, and operations required to fulfill a specific business requirement. Use cases interact with the data layer, perform validations, enforce business rules, and coordinate the execution of different components to achieve the desired outcome.\
A use case typically represents a specific scenario or a specific way in which a user interacts with the system to perform a task or achieve an objective. It focuses on the desired outcome or result and provides a high-level description of the interactions, inputs, and outputs involved.

1. proto file - could use cli generate add/server
2. proto file - cli/make api
3. update internal/conf/conf.proto and make config
4. update data.go file that under user/internal/data/, it controls db and data DI
5. update service, it is more like a controller layer call the biz.uc to achieve the goal(uc or usecase is more like service layer)
6. update service/service.go to make sure you put your service in wire.NewSet
7. update biz/user.go for business logic
8. update biz.go for wire
9. update data/user.go define struct mapping db schema (or you can define request body here to interact with external service)
