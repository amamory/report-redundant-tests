#include "gtest/gtest.h"
#include "cond_cov.cpp"

TEST(CondTest,fff)
{
    EXPECT_EQ(0,Condition_Cov(false,false,false));
};

TEST(CondTest,fft)
{
    EXPECT_EQ(0,Condition_Cov(false,false,true));
};

TEST(CondTest,ftf)
{
    EXPECT_EQ(0,Condition_Cov(false,true,false));
};

TEST(CondTest,ftt)
{
    EXPECT_EQ(1,Condition_Cov(false,true,true));
};

TEST(CondTest,tff)
{
    EXPECT_EQ(0,Condition_Cov(true,false,false));
};

TEST(CondTest,tft)
{
    EXPECT_EQ(1,Condition_Cov(true,false,true));
};

TEST(CondTest,ttf)
{
    EXPECT_EQ(0,Condition_Cov(true,true,false));
};

TEST(CondTest,ttt)
{
    EXPECT_EQ(1,Condition_Cov(true,true,true));
};


int main(int argc,char**argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}