#include "gtest/gtest.h"
#include "greatest.cpp"

TEST(GreaterTest,AisGreater)
{
    EXPECT_EQ(3,Greatest(3,1,2));
};

// this is a redundant test compared to 'AisGreater'
TEST(GreaterTest,AisGreaterRedundant)
{
    EXPECT_EQ(4,Greatest(4,1,2));
};

TEST(GreaterTest,BisGreater)
{
    EXPECT_EQ(3,Greatest(1,3,2));
};

TEST(GreaterTest,CisGreater)
{
    EXPECT_EQ(3,Greatest(1,2,3));
};

int main(int argc,char**argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}